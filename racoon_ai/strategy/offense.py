#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

import math
from logging import getLogger

from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.observer import Observer


class Offense:
    """Offense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer) -> None:
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
        cmd = self.__straight2ball(bot)
        self.__send_cmds.append(cmd)

    def __straight2ball(self, robot: Robot) -> RobotCommand:
        """straight2ball"""
        radian_ball_robot = radian_normalize(radian(self.__observer.ball, robot) - robot.theta)
        distance_target_robot = distance(self.__observer.ball, robot)
        speed = distance_target_robot / 1000.0

        # スピード制限
        speed = min(speed, 1)

        command = RobotCommand(5)
        command.vel_fwd = math.cos(radian_ball_robot) * speed
        command.vel_sway = math.sin(radian_ball_robot) * speed
        command.vel_angular = radian_ball_robot
        command.dribble_pow = 0
        command.kickpow = 0
        return command
