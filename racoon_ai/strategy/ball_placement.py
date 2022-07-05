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
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from .base import StrategyBase
from .role import Role


class BallPlacement(StrategyBase):
    """BallPlacement(StrategyBase)

    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, controls: Controls) -> None:
        super().__init__(observer, controls, role)

        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")

        self.__move_to_ball: bool = False
        self.__is_arrived: bool = False
        self.__is_fin: bool = False
        self.__wait_counter: int = 0

    def main(self) -> RobotCommand:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        # find nearest to ball robot
        point: Point = Point(-1500, 0, 0)
        bot = self.observer.get_our_by_id(5)
        if not bot:
            return RobotCommand(1)

        target_pose: Pose
        # 2点間の中心座標を算出
        target_pose = Pose((point.x + self.observer.ball.x) / 2, (point.y + self.observer.ball.y) / 2, 0)

        # ロボットがtarget_poseに近づいたら
        if MU.distance(target_pose, bot) < 10:
            self.__move_to_ball = True

        if self.__move_to_ball:
            target_pose = Pose(self.observer.ball.x, self.observer.ball.y, 0)

        cmd = self.controls.pid(target_pose, bot, 0.5)
        cmd.dribble_pow = float(1)

        if bot.is_ball_catched:
            target_pose = Pose(point.x, point.y, 0)
            cmd = self.controls.pid(target_pose, bot, 0.3)
            cmd.dribble_pow = float(1)

            if MU.distance(target_pose, bot) < 10:
                self.__is_arrived = True
                self.__logger.info("Arrived")

        if self.__is_arrived:
            target_pose = Pose(point.x - 125 * cos(bot.theta), point.y - 125 * sin(bot.theta), 0)
            cmd = self.controls.pid(target_pose, bot)
            cmd.dribble_pow = True

            if MU.distance(target_pose, bot) < 10:
                self.__wait_counter += 1
                cmd.dribble_pow = False
                if self.__wait_counter > 100:
                    self.__is_fin = True

        if self.__is_fin:
            target_pose = Pose(point.x - 300 * cos(bot.theta), point.y - 300 * sin(bot.theta), 0)
            cmd = self.controls.pid(target_pose, bot)
            cmd.dribble_pow = False

        cmd.vel_angular = bot.radian_ball_robot
        return cmd
