#!/usr/bin/env python3.10

"""out_of_play.py

    This module contains:
        - OutOfPlay
"""

from logging import getLogger
from math import cos, sin
from typing import Optional

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls, reset_all_imu
from racoon_ai.observer import Observer

from ..role import Role, SubRole
from .base import StrategyBase


class OutOfPlay(StrategyBase):
    """OutOfPlay(StrategyBase)

    Args:
        observer (Observer): Observer instance
        role (Role): Role instance
        subrole (SubRole): SubRole instance
        controls (Controls): Controls instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, subrole: SubRole, controls: Controls) -> None:
        super().__init__(observer, controls, role)

        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")

        self.__subrole = subrole

        self.__move_to_ball: bool = False
        self.__is_arrived: bool = False
        self.__is_fin: bool = False
        self.__wait_counter: int = 0
        self.__maintenance_point: float = -1  # Time out position (1: Plus in Y axis, -1: Minus in Y axis)

        self.__goal: Point = self.observer.geometry.goal
        self.__their_goal: Point = self.observer.geometry.their_goal
        self.__attack_direction: float = self.observer.attack_direction
        self.__center_circle_radius: float = self.observer.geometry.center_circle_radius

        # self.__stop_count: int = stop_count  # Roop counter

    def reset_imu(self, without_attacker: bool = False) -> None:
        """reset_imu"""
        self.__logger.debug("Reset IMU by camera theta ...")

        self.send_cmds = []

        target_bot_set: set[Robot] = set()
        if not without_attacker:
            target_bot_set = self.observer.our_robots_available

        else:
            for bot in self.observer.our_robots_available:
                if not bot:
                    continue
                if bot.robot_id == self.__subrole.our_attacker_id:
                    continue
                target_bot_set.add(bot)

        cmds: list[RobotCommand] = reset_all_imu(target_bot_set)
        self.send_cmds += cmds

    def reset_flag(self) -> None:
        """reset_flag"""
        self.__move_to_ball = False
        self.__is_arrived = False
        self.__is_fin = False
        self.__wait_counter = 0

    def placement_our(self) -> None:
        """placement_our"""
        self.__logger.debug("Placement...")

        self.send_cmds = []  # リスト初期化
        bot: Optional[Robot]

        # find nearest to ball robot
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            if point := self.observer.referee.placement_designated_point:
                # 2点間の中心座標を算出
                radian_ball_robot: float = MU.radian(self.observer.ball, bot)
                target_pose: Pose = Pose(
                    (point.x + self.observer.ball.x) / 2, (point.y + self.observer.ball.y) / 2, radian_ball_robot
                )

                cmd = self.controls.pid(target_pose, bot, 0.2)
                # ロボットがtarget_poseに近づいたら
                if MU.distance(target_pose, bot) < 60:
                    self.__move_to_ball = True

                if self.__move_to_ball:
                    self.__logger.info("Move to ball...")
                    # target_pose = Pose(self.observer.ball.x, self.observer.ball.y, bot.radian_ball_robot + bot.theta)
                    # cmd = self.controls.pid(target_pose, bot, 0.1)
                    radian_ball_point: float = MU.radian(self.observer.ball, point)
                    distance_robot_point: float = MU.distance(self.observer.ball, point)
                    target_pose = Pose(
                        self.observer.ball.x + distance_robot_point * cos(radian_ball_point),
                        self.observer.ball.y + distance_robot_point * sin(radian_ball_point),
                    )
                    cmd = self.controls.ball_around(target_pose, bot)
                    cmd = self.controls.speed_limiter(cmd, 0.1)

                cmd.dribble_pow = float(1)

                if bot.is_ball_catched:
                    self.__logger.info("Catch ball...")
                    target_pose = Pose(point.x, point.y, MU.radian(self.observer.ball, point))
                    cmd = self.controls.pid(target_pose, bot, 0.1)
                    cmd.dribble_pow = float(1)

                    if MU.distance(target_pose, bot) < 60:
                        target_pose = Pose(point.x, point.y, MU.radian(self.observer.ball, point))
                        cmd = self.controls.pid(target_pose, bot, 0.1)
                        self.__is_arrived = True
                        self.__logger.info("Arrived")

                if self.__is_arrived:
                    target_pose = Pose(bot.x, bot.y, MU.radian(self.observer.ball, point))
                    self.__wait_counter += 1
                    cmd.dribble_pow = False
                    cmd = RobotCommand(255)
                    if self.__wait_counter > 100:
                        self.__is_fin = True

                if self.__is_fin:
                    target_pose = Pose(
                        point.x - 300 * cos(bot.theta),
                        point.y - 300 * sin(bot.theta),
                        MU.radian(self.observer.ball, point),
                    )
                    cmd = self.controls.pid(target_pose, bot, 0.2)
                    cmd.dribble_pow = False

                cmd.vel_angular = bot.radian_ball_robot + bot.theta
                self.send_cmds += [cmd]
                return

            self.__logger.error("No designated point registered ...")

    def placement_their(self) -> None:
        """placement_their"""
        self.__logger.debug("Placement...")

        self.send_cmds = []  # リスト初期化
        bot: Optional[Robot]
        point: Optional[Point]

        # find nearest to ball robot
        if point := self.observer.referee.placement_designated_point:
            for bot in self.observer.our_robots_available:
                if bot.robot_id == self.role.keeper_id:
                    continue

                base_point = Point((point.x + self.observer.ball.x) / 2, (point.y + self.observer.ball.y) / 2)
                avoid_distance = MU.distance(self.observer.ball, base_point) + 1000
                cmd: RobotCommand = self.controls.make_command(bot)
                cmd = self.controls.avoid_point(cmd, bot, base_point, avoid_distance)
                cmd = self.controls.avoid_ball(cmd, bot, base_point)
                cmd = self.controls.avoid_enemy(cmd, bot, base_point)
                cmd = self.controls.speed_limiter(cmd)
                self.send_cmds += [cmd]

    def time_out(self) -> list[RobotCommand]:
        """placement_our"""
        self.__logger.debug("Placement...")

        self.send_cmds = []  # リスト初期化
        bot: Optional[Robot]

        target_pose = Pose(
            -self.observer.geometry.field_length / 2 * self.observer.attack_direction,
            self.observer.geometry.field_width / 2 * self.__maintenance_point,
            0,
        )

        for bot in self.observer.our_robots_available:
            cmd = self.controls.pid(target_pose, bot)
            cmd = self.controls.avoid_enemy(cmd, bot, target_pose)
            self.send_cmds += [cmd]
            target_pose.x += 500 * self.observer.attack_direction

        return self.send_cmds

    def pre_kick_off_offense(self, is_our: bool = False) -> None:
        """pre_kick_off_offense"""

        self.send_cmds = []

        for i, bot_id in enumerate(self.role.offense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                if bot.robot_id == self.__subrole.our_attacker_id:
                    if is_our:
                        target_pose = Pose(
                            0 - 130 * self.__attack_direction,
                            0,
                            MU.radian(self.__their_goal, self.__goal),
                        )
                        cmd = self.controls.pid(target_pose, bot)
                        # cmd = self.controls.avoid_ball(cmd, bot, target_pose)
                        self.send_cmds += [cmd]
                        continue

                    target_pose = Pose(
                        self.observer.ball.x - self.__center_circle_radius * 1.2 * self.__attack_direction,
                        self.observer.ball.y,
                        MU.radian(self.__their_goal, self.__goal),
                    )
                    cmd = self.controls.pid(target_pose, bot)
                    # cmd = self.controls.avoid_ball(cmd, bot, target_pose)

                else:
                    target_pose = Pose(
                        -600 * self.__attack_direction,
                        self.observer.geometry.field_width / 2 * (1 - 0.5 * (i + 1)),
                        MU.radian(self.__their_goal, self.__goal),
                    )
                    cmd = self.controls.pid(target_pose, bot)
                    cmd = self.controls.avoid_ball(cmd, bot, target_pose)
                cmd = self.controls.avoid_enemy(cmd, bot, target_pose)
                cmd = self.controls.speed_limiter(cmd)
                self.send_cmds += [cmd]

    def penalty_position(self, *, is_our: bool) -> None:
        """prep_penalty_kick"""

        self.send_cmds = []
        ignore_robot_id: int = self.__subrole.our_attacker_id if is_our else self.role.keeper_id
        revers: int = -1 if is_our else 1

        for bot in self.observer.our_robots_available:
            if bot.robot_id == ignore_robot_id:
                continue

            target_pose = Pose(
                self.observer.geometry.field_length / 2 * self.__attack_direction * revers,
                bot.y,
                0,
            )
            cmd: RobotCommand = self.controls.pid(target_pose, bot)
            cmd = self.controls.avoid_ball(cmd, bot, target_pose)
            cmd = self.controls.avoid_enemy(cmd, bot, target_pose)
            cmd = self.controls.speed_limiter(cmd)
            self.send_cmds += [cmd]
