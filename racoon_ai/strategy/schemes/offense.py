#!/usr/bin/env python3.10

"""offense.py

    This module contains:
        - Offense
"""

from logging import getLogger
from math import cos, sin
from typing import Optional

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from ..role import Role, SubRole
from .base import StrategyBase


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
        # self.__goal: Point = self.observer.geometry.goal
        # self.__their_goal: Point = self.observer.geometry.their_goal
        # self.__attack_direction: float = self.observer.attack_direction

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: Optional[RobotCommand]

        for i in range(self.role.get_offense_quantity):
            if bot := self.observer.get_our_by_id(self.role.get_offense_id(i)):
                if bot.robot_id == self.__subrole.our_attacker_id:
                    self.shoot_to_goal()
                    continue

                cmd = RobotCommand(bot.robot_id)
                self.send_cmds += [cmd]

    def shoot_to_goal(self) -> None:
        """shoot_to_goal"""
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            cmd = self.controls.ball_around(self.observer.geometry.their_goal, bot)
            if bot.distance_ball_robot <= 105 and (
                abs(MU.radian(self.observer.geometry.their_goal, bot) - bot.theta) < 0.1
            ):
                cmd.kickpow = 10
            cmd = self.controls.avoid_penalty_area(cmd, bot)
            cmd = self.controls.avoid_enemy(cmd, bot, self.observer.geometry.their_goal)
            cmd = self.controls.speed_limiter(cmd)
            self.send_cmds += [cmd]

    def stop_offense(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        for i in range(self.role.get_offense_quantity):
            if bot := self.observer.get_our_by_id(self.role.get_offense_id(i)):
                if bot.robot_id != self.__subrole.our_attacker_id:
                    radian_goal_ball = MU.radian(self.observer.geometry.their_goal, self.observer.ball)
                    radian_ball_robot = MU.radian(self.observer.ball, bot)
                    target_pose = Pose(
                        (self.observer.ball.x - 600 * cos(radian_goal_ball)),
                        (self.observer.ball.y - 600 * sin(radian_goal_ball)),
                        radian_ball_robot,
                    )
                    cmd = self.controls.pid(target_pose, bot)
                else:
                    cmd = RobotCommand(bot.robot_id)

                cmd = self.controls.avoid_ball(cmd, bot, self.observer.geometry.their_goal)
                cmd = self.controls.avoid_enemy(cmd, bot, self.observer.ball)
                cmd = self.controls.avoid_penalty_area(cmd, bot)
                cmd = self.controls.speed_limiter(cmd)
                self.send_cmds.append(cmd)

    def penalty_kick(self, pre_kick: bool = False) -> None:
        """penalty_kick"""
        self.send_cmds = []
        cmd: RobotCommand
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            if pre_kick:
                cmd = self.controls.to_front_ball(self.observer.geometry.their_goal, bot)
                self.send_cmds += [cmd]
                return

            self.shoot_to_goal()
