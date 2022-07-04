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
from racoon_ai.models.coordinate import Pose
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
        self.__standard_distance_penalty: float = 200**2
        # self.__max_robot_radius: float = 90

    def pid(self, target: Pose, bot: Robot, limiter: float = 1) -> RobotCommand:  # pylint: disable=R0914
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
    def speed_limiter(cmd: RobotCommand, limiter: float = 1) -> RobotCommand:
        """speed_limiter"""

        adjustment: float = sqrt(cmd.vel_sway**2 + cmd.vel_fwd**2)

        if adjustment > limiter >= 0:
            cmd.vel_sway = cmd.vel_sway / adjustment * limiter
            cmd.vel_fwd = cmd.vel_fwd / adjustment * limiter

        return cmd

    def avoid_enemy(self, cmd: RobotCommand, bot: Robot, target_pose: Pose) -> RobotCommand:
        """avoid_enemy"""

        radian_target_robot = MU.radian(target_pose, bot)
        distance_robot_target = MU.distance(bot, target_pose)

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        for enemy in self.__observer.enemy_robots:
            distance_enemy_target = MU.distance(enemy, target_pose)
            if enemy.is_visible is True and distance_enemy_target < distance_robot_target:
                radian_enemy_robot = MU.radian(enemy, bot)
                distance_enemy_robot = MU.distance(enemy, bot)
                bvel: NDArray[float64] = array(
                    [
                        self.__standard_distance_enemy
                        * cos(
                            radian_enemy_robot
                            - (MU.HALF_PI * sign(MU.radian_reduce(radian_enemy_robot, radian_target_robot)))
                        )
                        / (distance_enemy_robot**2),
                        self.__standard_distance_enemy
                        * sin(
                            radian_enemy_robot
                            - (MU.HALF_PI * sign(MU.radian_reduce(radian_enemy_robot, radian_target_robot)))
                        )
                        / (distance_enemy_robot**2),
                    ],
                    dtype=float64,
                )
                vel: NDArray[float64] = dot(bvel, rot_theta)
                cmd.vel_fwd += vel[0]
                cmd.vel_sway += vel[1]

        return cmd

    def avoid_penalty_area(self, cmd: RobotCommand, bot: Robot) -> RobotCommand:
        """avoid_penalty_erie"""

        rot_theta: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta)],
                [sin(bot.theta), cos(bot.theta)],
            ],
            dtype=float64,
        )

        theta = MU.radian(bot, self.__observer.geometry.goal)
        robot_dis = MU.distance(bot, self.__observer.geometry.goal)
        if abs(theta) < (MU.PI / 4):
            distance_robot_penalty = robot_dis - (self.__observer.geometry.goal_width / cos(theta))
        else:
            distance_robot_penalty = robot_dis - abs(self.__observer.geometry.goal_width / sin(theta))
        bvel_our: NDArray[float64] = array(
            [
                self.__standard_distance_penalty / (distance_robot_penalty**2) * cos(theta),
                self.__standard_distance_penalty / (distance_robot_penalty**2) * sin(theta),
            ],
            dtype=float64,
        )
        vel_our: NDArray[float64] = dot(bvel_our, rot_theta)
        cmd.vel_fwd += vel_our[0]
        cmd.vel_sway += vel_our[1]

        theta = MU.radian_reduce(MU.radian(bot, self.__observer.geometry.their_goal), MU.PI)
        robot_dis = MU.distance(bot, self.__observer.geometry.their_goal)
        if abs(theta) < (MU.PI / 4):
            distance_robot_penalty = robot_dis - (self.__observer.geometry.goal_width / cos(theta))
        else:
            distance_robot_penalty = robot_dis - abs(self.__observer.geometry.goal_width / sin(theta))
        bvel_their: NDArray[float64] = array(
            [
                self.__standard_distance_penalty / (distance_robot_penalty**2) * -1 * cos(theta),
                self.__standard_distance_penalty / (distance_robot_penalty**2) * -1 * sin(theta),
            ],
            dtype=float64,
        )
        vel_their: NDArray[float64] = dot(bvel_their, rot_theta)
        cmd.vel_fwd += vel_their[0]
        cmd.vel_sway += vel_their[1]

        return cmd
