#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

from logging import getLogger
from math import cos, sin
from typing import Optional

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from .base import StrategyBase
from .role import Role


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

        self.__role: Role = role
        self.__controls: Controls = controls

        self.__radius: float = self.observer.geometry.goal_width_half + self.observer.geometry.max_robot_radius

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        bot = self.observer.get_our_by_id(self.__role.keeper_id)

        if bot:
            self.__logger.debug(bot)
            cmd = self.__keep_goal(bot)
            self.send_cmds.append(cmd)

    def __keep_goal(self, robot: Robot) -> RobotCommand:
        """keep_goal"""
        radian_ball_goal = MU.radian(self.observer.ball, self.observer.geometry.goal)
        radian_ball_robot = MU.radian(self.observer.ball, robot)

        if abs(radian_ball_goal) >= MU.PI / 2:
            radian_ball_goal = (sign(radian_ball_goal) * MU.PI) / 2
        target_pose = Pose(
            (self.observer.geometry.goal.x + self.__radius * cos(radian_ball_goal)),
            (self.observer.geometry.goal.y + self.__radius * sin(radian_ball_goal)),
            radian_ball_robot,
        )

        command: RobotCommand = self.__controls.pid(target_pose, robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command
