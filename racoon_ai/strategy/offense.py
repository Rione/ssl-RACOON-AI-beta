#!/usr/bin/env python3.10

"""offense.py

    This module contains:
        - Offense
"""

from logging import getLogger
from math import cos, sin, sqrt
from typing import Optional

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
                    cmd = self.__ballaround(bot)
                    if (
                        bot.distance_ball_robot <= 105
                        and abs(MU.radian(self.observer.geometry.their_goal, bot) - bot.theta) < 0.1
                    ):
                        cmd.kickpow = 10
                    cmd = self.controls.avoid_enemy(cmd, bot, Pose(self.observer.ball.x, self.observer.ball.y))
                    cmd = self.controls.avoid_penalty_area(cmd, bot)
                    cmd = self.controls.speed_limiter(cmd)
                    self.send_cmds.append(cmd)
                else:
                    cmd = RobotCommand(bot.robot_id)
                    cmd.vel_fwd = 0
                    cmd.vel_sway = 0
                    cmd.vel_angular = 0
                    self.send_cmds.append(cmd)

    def __ballaround(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_goal_robot: float = MU.radian_reduce(MU.radian(self.observer.geometry.their_goal, robot), robot.theta)
        adjustment: float = robot.distance_ball_robot / 900

        vel_fwd: float = cos(robot.radian_ball_robot) * adjustment
        vel_sway: float = sin(robot.radian_ball_robot) * adjustment

        radian_around: float = MU.radian(self.observer.ball, robot)
        discrimination: float = MU.radian_reduce(
            MU.radian(robot, self.observer.ball),
            MU.radian(self.observer.geometry.their_goal, self.observer.ball),
        )
        radian_around -= ((discrimination / MU.div_safe(abs(discrimination))) * MU.PI) / 2
        radian_around -= robot.theta
        adjustment = 100 / MU.div_safe(robot.distance_ball_robot)

        vel_fwd += cos(radian_around) * adjustment
        vel_sway += sin(radian_around) * adjustment

        discrimination = MU.radian_reduce(
            MU.radian(self.observer.ball, robot),
            MU.radian(self.observer.geometry.their_goal, robot),
        )
        adjustment = 0.1 / MU.div_safe(abs(discrimination))

        vel_fwd += cos(robot.radian_ball_robot) * adjustment
        vel_sway += sin(robot.radian_ball_robot) * adjustment

        adjustment = MU.div_safe(sqrt(vel_fwd * vel_fwd + vel_sway * vel_sway))
        speed = robot.distance_ball_robot / 500

        command = RobotCommand(robot.robot_id)
        command.vel_fwd = speed * vel_fwd / adjustment
        command.vel_sway = speed * vel_sway / adjustment
        command.vel_angular = radian_goal_robot
        return command
