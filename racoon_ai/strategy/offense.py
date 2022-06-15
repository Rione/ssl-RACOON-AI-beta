#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

import math
from logging import getLogger

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU

# from racoon_ai.models.coordinate import Point, Pose
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
        print(bot.x)
        if (
            abs(MU.radian(self.__observer.goal, bot) - bot.theta) < 0.1
            and MU.distance(self.__observer.ball, bot) <= 105
        ):
            cmd.kickpow = 10
        # print(distance(self.__observer.ball, bot))
        self.__send_cmds.append(cmd)

    def __ballaround(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        radian_goal_robot = MU.radian_normalize(MU.radian(self.__observer.goal, robot) - robot.theta)
        distance_target_robot = MU.distance(self.__observer.ball, robot)
        adjustment = distance_target_robot / 900

        vel_fwd = math.cos(radian_ball_robot) * adjustment
        vel_sway = math.sin(radian_ball_robot) * adjustment

        radian_around = MU.radian_normalize(MU.radian(self.__observer.ball, robot))
        discrimination = MU.radian_normalize(
            MU.radian_normalize(MU.radian(robot, self.__observer.ball))
            - MU.radian_normalize(MU.radian(self.__observer.goal, self.__observer.ball))
        )
        radian_around -= sign(discrimination) * math.pi / 2
        radian_around -= robot.theta
        adjustment = 100 / distance_target_robot

        vel_fwd += math.cos(radian_around) * adjustment
        vel_sway += math.sin(radian_around) * adjustment

        discrimination = MU.radian_normalize(
            MU.radian_normalize(MU.radian(self.__observer.ball, robot))
            - MU.radian_normalize(MU.radian(self.__observer.goal, robot))
        )
        adjustment = 0.1 / abs(discrimination)

        vel_fwd += math.cos(radian_ball_robot) * adjustment
        vel_sway += math.sin(radian_ball_robot) * adjustment

        adjustment = math.sqrt(vel_fwd * vel_fwd + vel_sway * vel_sway)
        speed = distance_target_robot / 1000.0
        speed = min(speed, 0.3)

        command = RobotCommand(5)
        command.vel_fwd = vel_fwd / adjustment * speed
        command.vel_sway = vel_sway / adjustment * speed
        command.vel_angular = radian_goal_robot
        command.dribble_pow = 0
        command.kickpow = 0
        return command
