#!/usr/bin/env python3.10

"""offense.py

    This module contains:
        - Offense
"""

from logging import getLogger
from typing import Optional

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from .base import StrategyBase
from .role import Role
from .subrole import SubRole


class Offense(StrategyBase):
    """Offense(StrategyBase)

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

        self.__subrole: SubRole = subrole

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: Optional[RobotCommand]

        for i in range(self.role.get_offense_quantity):
            if bot := self.observer.get_our_by_id(self.role.get_offense_id(i)):
                if bot.robot_id == self.__subrole.our_attacker_id:
                    cmd = self.controls.ball_around(self.observer.geometry.their_goal, bot)
                    if bot.distance_ball_robot <= 105 and (
                        abs(MU.radian(self.observer.geometry.their_goal, bot) - bot.theta) < 0.1
                    ):
                        cmd.kickpow = 10
                    cmd = self.controls.avoid_enemy(cmd, bot, self.observer.ball)
                    cmd = self.controls.avoid_penalty_area(cmd, bot)
                    cmd = self.controls.speed_limiter(cmd)
                    self.send_cmds += [cmd]
                    continue

                cmd = RobotCommand(bot.robot_id)
                self.send_cmds += [cmd]
