#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

from logging import getLogger
from math import cos, sin, sqrt

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver

# from racoon_ai.strategy.role import Role


class Offense:
    """Offense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: MWReceiver) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        # self.__role = role
        self.__send_cmds: list[RobotCommand]
        self.__kick_flag: bool = False
        # self.__arrive_flag: bool = False

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    @property
    def kick_flag(self) -> bool:
        """kick_flag

        Returns:
            bool: kick_flag
        """
        return self.__kick_flag

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.__send_cmds = []
        bot: Robot
        cmd: RobotCommand

        # 一番ボールに近いロボットがボールに向かって前進
        bot = self.__observer.our_robots[5]
        # if (
        #    distance(self.__observer.ball, bot) >= 150
        #    or abs(radian_normalize(radian(self.__our_goal, bot))
        #    - radian_normalize(radian(self.__observer.ball, bot)))
        #    <= 0.1
        # ):
        #    cmd = self.__straightball(bot)
        # elif distance(self.__observer.ball, bot) <= 105:
        #    cmd = self.__straightgoal(bot)
        # else:
        #    cmd = self.__ballaround(bot)

        # if abs(radian_normalize(radian(self.__our_goal, bot))
        # - radian_normalize(radian(self.__observer.ball, bot))) >= 0.1:
        #   cmd = self.__ballaround2(bot)
        # elif distance(self.__observer.ball, bot) <= 105:
        #    cmd = self.__straightgoal(bot)
        # else:
        #    cmd = self.__straightball(bot)

        cmd = self.__ballaround(bot)
        if bot.distance_ball_robot <= 105 and abs(MU.radian(self.__observer.geometry.goal, bot) - bot.theta) < 0.1:
            cmd.kickpow = 10
        self.__send_cmds.append(cmd)

    def __ballaround(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_goal_robot: float = MU.radian_reduce(MU.radian(self.__observer.geometry.goal, robot), robot.theta)
        adjustment: float = robot.distance_ball_robot / 900

        vel_fwd: float = cos(robot.radian_ball_robot) * adjustment
        vel_sway: float = sin(robot.radian_ball_robot) * adjustment

        radian_around: float = MU.radian(self.__observer.ball, robot)
        discrimination: float = MU.radian_reduce(
            MU.radian(robot, self.__observer.ball),
            MU.radian(self.__observer.geometry.goal, self.__observer.ball),
        )
        radian_around -= ((discrimination / MU.div_safe(abs(discrimination))) * MU.PI) / 2
        radian_around -= robot.theta
        adjustment = 100 / MU.div_safe(robot.distance_ball_robot)

        vel_fwd += cos(radian_around) * adjustment
        vel_sway += sin(radian_around) * adjustment

        discrimination = MU.radian_reduce(
            MU.radian(self.__observer.ball, robot),
            MU.radian(self.__observer.geometry.goal, robot),
        )
        adjustment = 0.1 / MU.div_safe(abs(discrimination))

        vel_fwd += cos(robot.radian_ball_robot) * adjustment
        vel_sway += sin(robot.radian_ball_robot) * adjustment

        adjustment = MU.div_safe(sqrt(vel_fwd * vel_fwd + vel_sway * vel_sway))
        speed = robot.distance_ball_robot / 1000.0
        speed = min(speed, 0.8)

        command = RobotCommand(5)
        command.vel_fwd = speed * vel_fwd / adjustment
        command.vel_sway = speed * vel_sway / adjustment
        command.vel_angular = radian_goal_robot
        return command
