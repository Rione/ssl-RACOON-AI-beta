#!/usr/bin/env python3.10

"""offense.py

    This module contains:
        - Offense
"""

from logging import getLogger
from typing import Optional
from math import cos, sin
from racoon_ai.common.math_utils import MathUtils as MU

from racoon_ai.models.coordinate import Pose
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

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, subrole: SubRole, controls: Controls) -> None:
        super().__init__(observer, controls, role)

        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__subrole: SubRole = subrole

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        for i in range(self.role.get_offense_quantity):
            bot = self.observer.get_our_by_id(self.role.get_offense_id(i))
            if bot:
                if bot.robot_id == self.__subrole.our_attacker_id:
                    cmd = self.controls.ball_around(self.observer.geometry.their_goal, bot)
                    if (
                        bot.distance_ball_robot <= 105
                        and abs(MU.radian(self.observer.geometry.their_goal, bot) - bot.theta) < 0.1
                    ):
                        cmd.kickpow = 10
                    # cmd = self.controls.avoid_enemy(cmd, bot, Pose(self.observer.ball.x, self.observer.ball.y))
                    # cmd = self.controls.avoid_penalty_area(cmd, bot)
                    cmd = self.controls.speed_limiter(cmd)
                    self.send_cmds.append(cmd)
                else:
                    cmd = RobotCommand(bot.robot_id)
                    self.send_cmds.append(cmd)

    def stop_offense(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        for i in range(self.role.get_offense_quantity):
            bot = self.observer.get_our_by_id(self.role.get_offense_id(i))
            if bot:
                if bot.robot_id == self.__subrole.our_attacker_id:
                    radian_goal_ball = MU.radian(self.observer.geometry.their_goal, self.observer.ball)
                    radian_ball_robot = MU.radian(self.observer.ball, bot)
                    target_pose = Pose(
                        (self.observer.ball.x - 600 * cos(radian_goal_ball)),
                        (self.observer.ball.y - 600 * sin(radian_goal_ball)),
                        radian_ball_robot,
                    )
                    cmd = self.controls.pid(target_pose, bot)
                    cmd = self.controls.avoid_ball(cmd, bot, target_pose)
                    print(bot.distance_ball_robot)
                    # cmd = self.controls.avoid_enemy(cmd, bot, Pose(self.observer.ball.x, self.observer.ball.y))
                    # cmd = self.controls.avoid_penalty_area(cmd, bot)
                    cmd = self.controls.speed_limiter(cmd)
                    self.send_cmds.append(cmd)
                else:
                    cmd = RobotCommand(bot.robot_id)
                    cmd = self.controls.avoid_ball(cmd, bot, self.observer.geometry.their_goal)
                    self.send_cmds.append(cmd)
