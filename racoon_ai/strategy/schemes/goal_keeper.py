#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

from logging import getLogger
from math import cos, sin
from typing import Optional

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from ..role import Role
from .base import StrategyBase


class Keeper(StrategyBase):
    """Keeper(StrategyBase)

    Args:
        observer (Observer): Observer instance
        role (Role): Role instance
        controls (Controls): Controls instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, controls: Controls) -> None:
        super().__init__(observer, controls, role)

        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")
        self.__radius: float = self.observer.geometry.goal_width_half + self.observer.geometry.max_robot_radius
        self.__goal: Point = self.observer.geometry.goal
        self.__their_goal: Point = self.observer.geometry.their_goal
        self.__attack_direction: float = self.observer.attack_direction

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        if bot := self.observer.get_our_by_id(self.role.keeper_id):
            self.__logger.debug(bot)
            cmd = self.__keep_goal(bot)
            self.send_cmds += [cmd]

    def __keep_goal(self, robot: Robot) -> RobotCommand:
        """keep_goal"""
        radian_ball_goal = MU.radian_reduce(
            MU.radian(self.observer.ball, self.__goal), MU.radian(self.__their_goal, self.__goal)
        )
        radian_ball_robot = MU.radian(self.observer.ball, robot)

        if abs(radian_ball_goal) >= MU.PI / 2:
            radian_ball_goal = (sign(radian_ball_goal) * MU.PI) / 2
        target_pose = Pose(
            (self.__goal.x + self.__radius * cos(radian_ball_goal) * self.__attack_direction),
            (self.__goal.y + self.__radius * sin(radian_ball_goal) * self.__attack_direction),
            radian_ball_robot,
        )

        return self.controls.pid(target_pose, robot)

    def to_goal_position(self) -> None:
        """to_goal_position"""
        self.send_cmds = []
        if bot := self.observer.get_our_by_id(self.role.keeper_id):
            target_pose = Pose(self.__goal.x, self.__goal.y, MU.radian(self.observer.ball, bot))

            cmd: RobotCommand = self.controls.pid(target_pose, bot)
            self.send_cmds += [cmd]
