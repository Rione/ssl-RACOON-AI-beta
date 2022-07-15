#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

from logging import getLogger
from math import cos, sin, sqrt
from typing import Tuple

from numpy import array, divide, dot, float64, multiply, sign, subtract, zeros
from numpy.typing import NDArray

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.observer import Observer


class Controls:
    """Controls
    Args:
        observer (Observer): Observer instance
        k_gain (Tuple[float, float, float]): PID gain (kp, ki, kd)

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, k_gain: Tuple[float, float, float] = (1, 0, 0)) -> None:
        self.__logger = getLogger(__name__)
        self.__observer: Observer = observer
        self.__dtaime: float = self.__observer.sec_per_frame
        self.__k_gain: NDArray[float64] = array(k_gain, dtype=float64)
        self.__pre_target_pose: NDArray[float64] = zeros((11, 3), dtype=float64)
        self.__pre_bot_pose: NDArray[float64] = zeros((11, 3), dtype=float64)
        self.__accumulations: NDArray[float64] = zeros((11, 3), dtype=float64)
        self.__pre_target_theta: NDArray[float64] = zeros((11,), dtype=float64)
        self.__pre_bot_theta: NDArray[float64] = zeros((11,), dtype=float64)
        self.__theta_accumulation: NDArray[float64] = zeros((11,), dtype=float64)
        self.__standard_distance_enemy: float = 500**2
        # self.__standard_distance_penalty: float = 350**2
        # self.__max_robot_radius: float = 90
        self.__attack_direction: float = self.__observer.attack_direction

    def pid(self, target: Pose, bot: Robot, limiter: float = 0.28) -> RobotCommand:  # pylint: disable=R0914
        """pid

        Apply PID control to the robot to reach the target pose.

        Args:
            target (Pose): Target pose
            bot (Robot): Robot instance
            limiter (float, optional): speed limit (default: 1, nolimit: -1)

        Returns:
            RobotCommand: RobotCommand instance
        """
        bot_id: int = int(bot.robot_id)
        cmd: RobotCommand = RobotCommand(bot_id, use_imu=bot.is_imu_enabled)
        bot_pose: NDArray[float64] = array([bot.x / 1000, bot.y / 1000, bot.theta], dtype=float64)
        target_pose: NDArray[float64] = array([target.x / 1000, target.y / 1000, target.theta], dtype=float64)

        bot_speed: NDArray[float64] = divide(
            subtract(bot_pose, self.__pre_bot_pose[bot_id], dtype=float64), self.__dtaime, dtype=float64
        )
        target_speed: NDArray[float64] = divide(
            subtract(target_pose, self.__pre_target_pose[bot_id], dtype=float64), self.__dtaime, dtype=float64
        )

        diff_pose: NDArray[float64] = subtract(target_pose, bot_pose, dtype=float64)
        diff_pose[2] = MU.radian_normalize(diff_pose[2])
        diff_speed: NDArray[float64] = subtract(target_speed, bot_speed, dtype=float64)

        self.__pre_bot_pose[bot_id] = bot_pose
        self.__pre_target_pose[bot_id] = target_pose

        self.__accumulations[bot_id] += multiply(diff_pose, self.__dtaime, dtype=float64)

        bbvel: NDArray[float64] = array([diff_pose, diff_speed, self.__accumulations[bot_id]], dtype=float64)
        bvel: NDArray[float64] = dot(self.__k_gain, bbvel)

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta), 0],
                [sin(bot.theta), cos(bot.theta), 0],
                [0, 0, 1],
            ],
            dtype=float64,
        )

        vel: NDArray[float64] = dot(bvel, rot_theta)

        cmd.vel_fwd = float(vel[0])
        cmd.vel_sway = float(vel[1])
        cmd.vel_angular = self.pid_radian(target.theta, bot)
        cmd.target_pose = target

        if not cmd.use_imu:
            cmd.vel_angular = self.pid_radian(target.theta, bot)
        cmd = self.speed_limiter(cmd, limiter)
        self.__logger.debug("cmd: %s", cmd)
        return cmd

    def pid_radian(self, target_theta: float, bot: Robot) -> float:
        """pid_radian

        Args:
            target_theta (float): Target theta
            bot (Robot): Robot instance
        """
        vel_angular: float = float(0)
        kp: float = float(self.__k_gain[0])
        kd: float = float(self.__k_gain[1])
        ki: float = float(self.__k_gain[2])
        bot_id: int = int(bot.robot_id)

        e_bot: float = bot.theta - self.__pre_bot_theta[bot_id]
        e_target: float = target_theta - self.__pre_target_theta[bot_id]
        self.__theta_accumulation += (e_target - e_bot) * self.__dtaime

        vel_angular += kp * (MU.radian_normalize(target_theta - bot.theta))
        vel_angular += kd * ((e_target / self.__dtaime) - (e_bot / self.__dtaime))
        vel_angular += ki * self.__theta_accumulation[bot_id]

        self.__pre_target_theta[bot_id] = target_theta
        self.__pre_bot_theta[bot_id] = bot.theta

        if vel_angular > MU.PI:
            vel_angular = min(vel_angular, MU.PI)
        elif vel_angular < -MU.PI:
            vel_angular = max(vel_angular, -MU.PI)

        self.__logger.debug("vel_angular: %s", vel_angular)
        return vel_angular

    @staticmethod
    def speed_limiter(cmd: RobotCommand, limiter: float = 0.20) -> RobotCommand:
        """speed_limiter"""
        if limiter <= 0:
            return cmd

        adjustment: float = sqrt(cmd.vel_sway**2 + cmd.vel_fwd**2)
        if adjustment <= limiter:
            return cmd

        cmd.vel_sway = (cmd.vel_sway / MU.div_safe(adjustment)) * limiter
        cmd.vel_fwd = (cmd.vel_fwd / MU.div_safe(adjustment)) * limiter
        return cmd

    def avoid_enemy(self, cmd: RobotCommand, bot: Robot, target_point: Point) -> RobotCommand:
        """avoid_enemy"""
        radian_target_robot = MU.radian(target_point, bot)
        distance_robot_target = MU.distance(bot, target_point)

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        for enemy in self.__observer.enemy_robots_available:
            if MU.distance(enemy, target_point) >= distance_robot_target:
                continue

            radian_enemy_robot: float = MU.radian(enemy, bot)
            distance_enemy_robot: float = MU.distance(enemy, bot)
            divisor: float = distance_enemy_robot**2
            bvel: NDArray[float64] = array(
                [
                    self.__standard_distance_enemy
                    * cos(
                        radian_enemy_robot
                        - (MU.HALF_PI * sign(MU.radian_reduce(radian_enemy_robot, radian_target_robot)))
                    )
                    / divisor,
                    self.__standard_distance_enemy
                    * sin(
                        radian_enemy_robot
                        - (MU.HALF_PI * sign(MU.radian_reduce(radian_enemy_robot, radian_target_robot)))
                    )
                    / divisor,
                ],
                dtype=float64,
            )
            vel: NDArray[float64] = dot(bvel, rot_theta)
            cmd.vel_fwd += vel[0]
            cmd.vel_sway += vel[1]
        return cmd

    def avoid_penalty_area(self, cmd: RobotCommand, bot: Robot, distance_penalty: float = 350) -> RobotCommand:
        """avoid_penalty_erie"""
        adjustment: float = 0
        distance_penalty = distance_penalty**2

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        theta: float = MU.radian_reduce(
            MU.radian(bot, self.__observer.geometry.goal),
            MU.radian(self.__observer.geometry.their_goal, self.__observer.geometry.goal),
        )
        robot_dis: float = MU.distance(bot, self.__observer.geometry.goal)
        if abs(theta) < (MU.PI / 4):
            distance_robot_penalty = robot_dis - (self.__observer.geometry.goal_width / cos(theta))
        else:
            distance_robot_penalty = robot_dis - abs(self.__observer.geometry.goal_width / sin(theta))
        adjustment = distance_penalty / (distance_robot_penalty**2)
        bvel_our: NDArray[float64] = array(
            [
                adjustment * cos(theta) * self.__attack_direction,
                adjustment * sin(theta) * self.__attack_direction,
            ],
            dtype=float64,
        )
        vel_our: NDArray[float64] = dot(bvel_our, rot_theta)
        cmd.vel_fwd += vel_our[0]
        cmd.vel_sway += vel_our[1]

        theta = MU.radian_reduce(
            MU.radian(bot, self.__observer.geometry.their_goal),
            MU.radian(self.__observer.geometry.goal, self.__observer.geometry.their_goal),
        )
        robot_dis = MU.distance(bot, self.__observer.geometry.their_goal)
        if abs(theta) < (MU.PI / 4):
            distance_robot_penalty = robot_dis - (self.__observer.geometry.goal_width / cos(theta))
        else:
            distance_robot_penalty = robot_dis - abs(self.__observer.geometry.goal_width / sin(theta))
        adjustment = distance_penalty / (distance_robot_penalty**2)
        bvel_their: NDArray[float64] = array(
            [
                adjustment * -1 * cos(theta) * self.__attack_direction,
                adjustment * -1 * sin(theta) * self.__attack_direction,
            ],
            dtype=float64,
        )

        vel_their: NDArray[float64] = dot(bvel_their, rot_theta)
        cmd.vel_fwd += vel_their[0]
        cmd.vel_sway += vel_their[1]
        return cmd

    def ball_around(self, target: Point, bot: Robot) -> RobotCommand:
        """ball_around"""
        radian_target_robot: float = MU.radian_reduce(MU.radian(target, bot), bot.theta)
        adjustment: float = bot.distance_ball_robot / 2000

        vel_fwd: float = cos(bot.radian_ball_robot) * adjustment
        vel_sway: float = sin(bot.radian_ball_robot) * adjustment

        radian_around: float = MU.radian(self.__observer.ball, bot)
        discrimination: float = MU.radian_reduce(
            MU.radian(bot, self.__observer.ball),
            MU.radian(target, self.__observer.ball),
        )
        radian_around -= (sin(discrimination) * MU.PI) / 2
        radian_around -= bot.theta
        adjustment = 280**2 / MU.div_safe(bot.distance_ball_robot**2)

        vel_fwd += cos(radian_around) * adjustment
        vel_sway += sin(radian_around) * adjustment

        discrimination = MU.radian_reduce(
            MU.radian(self.__observer.ball, bot),
            MU.radian(target, bot),
        )

        adjustment = (0.3 / MU.div_safe(abs(discrimination))) ** 2
        vel_fwd += cos(bot.radian_ball_robot) * adjustment
        vel_sway += sin(bot.radian_ball_robot) * adjustment

        adjustment = MU.div_safe(sqrt(vel_fwd * vel_fwd + vel_sway * vel_sway))
        speed = bot.distance_ball_robot / 500

        vel_fwd = speed * vel_fwd / adjustment
        vel_sway = speed * vel_sway / adjustment

        command = RobotCommand(bot.robot_id, use_imu=bot.is_imu_enabled)
        command.vel_fwd = vel_fwd
        command.vel_sway = vel_sway
        command.vel_angular = self.pid_radian(radian_target_robot + bot.theta, bot)
        command.target_pose.theta = radian_target_robot + bot.theta
        return command

    def avoid_ball(
        self, cmd: RobotCommand, bot: Robot, target_pose: Point, basic_distance: float = 500
    ) -> RobotCommand:
        """avoid_enemy"""

        radian_target_robot = MU.radian(target_pose, bot)
        avoid_distance = basic_distance**2

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        radian_ball_robot = MU.radian(self.__observer.ball, bot)
        distance_ball_robot = MU.distance(self.__observer.ball, bot)
        distance_target_robot = MU.distance(target_pose, bot) / 1000
        if distance_ball_robot < basic_distance:
            bvel: NDArray[float64] = array(
                [
                    avoid_distance
                    * distance_target_robot
                    * cos(
                        radian_ball_robot
                        - (MU.HALF_PI * sign(MU.radian_reduce(radian_ball_robot, radian_target_robot)))
                    )
                    / (distance_ball_robot**2),
                    avoid_distance
                    * distance_target_robot
                    * sin(
                        radian_ball_robot
                        - (MU.HALF_PI * sign(MU.radian_reduce(radian_ball_robot, radian_target_robot)))
                    )
                    / (distance_ball_robot**2),
                ],
                dtype=float64,
            )
            vel: NDArray[float64] = dot(bvel, rot_theta)
            cmd.vel_fwd += vel[0]
            cmd.vel_sway += vel[1]

        return cmd

    def to_front_ball(self, target_point: Point, bot: Robot, leave_distance: float = 130) -> RobotCommand:
        """to_front_ball"""
        radian_point_ball = MU.radian(target_point, self.__observer.ball)
        target_pose = Pose(
            self.__observer.ball.x - leave_distance * cos(radian_point_ball),
            self.__observer.ball.y - leave_distance * sin(radian_point_ball),
            radian_point_ball,
        )
        cmd = self.pid(target_pose, bot)
        cmd = self.avoid_ball(cmd, bot, target_pose, leave_distance * 1.2)
        cmd = self.avoid_enemy(cmd, bot, target_pose)
        cmd = self.speed_limiter(cmd)
        return cmd

    @staticmethod
    def avoid_point(cmd: RobotCommand, bot: Robot, target_point: Point, basic_distance: float) -> RobotCommand:
        """avoid_point"""
        avoid_distance = basic_distance**2

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        radian_robot_point = MU.radian(bot, target_point)
        distance_robot_point = MU.distance(bot, target_point)
        adjustment: float = avoid_distance / (distance_robot_point**2) - 1
        adjustment = max(adjustment, 0)
        bvel: NDArray[float64] = array(
            [adjustment * cos(radian_robot_point), adjustment * sin(radian_robot_point)],
            dtype=float64,
        )
        vel: NDArray[float64] = dot(bvel, rot_theta)
        cmd.vel_fwd += vel[0]
        cmd.vel_sway += vel[1]

        return cmd

    @staticmethod
    def make_command(bot: Robot) -> RobotCommand:
        """make_command"""
        return RobotCommand(bot.robot_id, use_imu=bot.is_imu_enabled)
