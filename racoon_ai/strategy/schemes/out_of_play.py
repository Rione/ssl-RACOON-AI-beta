#!/usr/bin/env python3.10

"""ball_placement.py

    This module contains:
        - BallPlacement
"""

from logging import getLogger
from math import cos, sin
from typing import Optional

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot
from racoon_ai.models.robot.commands import RobotCommand
from racoon_ai.movement import Controls
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
        self.__logger.info("Initializing...")

        self.__subrole = subrole

        self.__move_to_ball: bool = False
        self.__is_arrived: bool = False
        self.__is_fin: bool = False
        self.__wait_counter: int = 0

    def placement_our(self) -> None:
        """placement_our"""
        self.__logger.debug("Placement...")

        self.send_cmds = []  # リスト初期化
        bot: Optional[Robot]
        # find nearest to ball robot
        if bot := self.observer.our_robots[0]:
            point: Point = Point(0, 0)
            # 2点間の中心座標を算出
            radian_ball_robot = MU.radian(self.observer.ball, bot)
            target_pose = Pose(
                (point.x + self.observer.ball.x) / 2, (point.y + self.observer.ball.y) / 2, radian_ball_robot
            )

            cmd = self.controls.pid(target_pose, bot, 0.3)
            # ロボットがtarget_poseに近づいたら
            if MU.distance(target_pose, bot) < 50:
                self.__move_to_ball = True

            if self.__move_to_ball:
                self.__logger.info("Move to ball...")
                # target_pose = Pose(self.observer.ball.x, self.observer.ball.y, bot.radian_ball_robot + bot.theta)
                # cmd = self.controls.pid(target_pose, bot, 0.1)
                radian_ball_point = MU.radian(self.observer.ball, point)
                distance_robot_point = MU.distance(self.observer.ball, point)
                target_pose = Point(
                    self.observer.ball.x + distance_robot_point * cos(radian_ball_point),
                    self.observer.ball.y + distance_robot_point * sin(radian_ball_point),
                )
                cmd = self.controls.ball_around(target_pose, bot)
                cmd = self.controls.speed_limiter(cmd, 0.2)

            cmd.dribble_pow = float(1)

            if bot.is_ball_catched:
                self.__logger.info("Catch ball...")
                target_pose = Pose(point.x, point.y, MU.radian(self.observer.ball, point))
                cmd = self.controls.pid(target_pose, bot, 0.1)
                cmd.dribble_pow = float(1)

                if MU.distance(target_pose, bot) < 50:
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
                    point.x - 300 * cos(bot.theta), point.y - 300 * sin(bot.theta), MU.radian(self.observer.ball, point)
                )
                cmd = self.controls.pid(target_pose, bot, 0.3)
                cmd.dribble_pow = False

            cmd.vel_angular = bot.radian_ball_robot + bot.theta
            # print(cmd)
            self.send_cmds += [cmd]
