#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

from logging import getLogger
from math import cos, sin, sqrt
from typing import Optional

from racoon_ai.common.math_utils import MathUtils as MU

# from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement.controls import Controls
from racoon_ai.observer import Observer
from racoon_ai.strategy.role import Role
from racoon_ai.strategy.subrole import SubRole


class Offense:
    """Offense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, subrole: SubRole, controls: Controls) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer: Observer = observer
        self.__role = role
        self.__subrole = subrole
        self.__controls = controls
        self.__send_cmds: list[RobotCommand] = []

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.__send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        for i in range(self.__role.get_offense_quantity):
            bot = self.__observer.get_our_by_id(self.__role.get_offense_id(i))
            if bot:
                if bot.robot_id == self.__subrole.our_attacker_id:
                    cmd = self.__ballaround(bot)
                    if (
                        bot.distance_ball_robot <= 105
                        and abs(MU.radian(self.__observer.geometry.their_goal, bot) - bot.theta) < 0.1
                    ):
                        cmd.kickpow = 10
                    # cmd = self.__controls.avoid_enemy(cmd, bot, Pose(self.__observer.ball.x, self.__observer.ball.y))
                    cmd = self.__controls.avoid_penalty_area(cmd, bot)
                    cmd = self.__controls.speed_limiter(cmd)
                    self.__send_cmds.append(cmd)
                else:
                    cmd = RobotCommand(bot.robot_id)
                    cmd.vel_fwd = 0
                    cmd.vel_sway = 0
                    cmd.vel_angular = 0
                    self.__send_cmds.append(cmd)

    def __ballaround(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_goal_robot: float = MU.radian_reduce(MU.radian(self.__observer.geometry.their_goal, robot), robot.theta)
        adjustment: float = robot.distance_ball_robot / 900

        vel_fwd: float = cos(robot.radian_ball_robot) * adjustment
        vel_sway: float = sin(robot.radian_ball_robot) * adjustment

        radian_around: float = MU.radian(self.__observer.ball, robot)
        discrimination: float = MU.radian_reduce(
            MU.radian(robot, self.__observer.ball),
            MU.radian(self.__observer.geometry.their_goal, self.__observer.ball),
        )
        radian_around -= ((discrimination / MU.div_safe(abs(discrimination))) * MU.PI) / 2
        radian_around -= robot.theta
        adjustment = 100 / MU.div_safe(robot.distance_ball_robot)

        vel_fwd += cos(radian_around) * adjustment
        vel_sway += sin(radian_around) * adjustment

        discrimination = MU.radian_reduce(
            MU.radian(self.__observer.ball, robot),
            MU.radian(self.__observer.geometry.their_goal, robot),
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
