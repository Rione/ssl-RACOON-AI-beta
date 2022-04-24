#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

import math
from logging import getLogger

from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.observer import Observer


class Keeper:
    """Keeper
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
        # self.__arrive_flag: bool = False
        self.__our_goal: Point = Point(-6000, 0)
        self.__radius: float = 600

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
        bot: Robot
        cmd: RobotCommand

        # 一番ボールに近いロボットがボールに向かって前進
        bot = self.__observer.our_robots[0]
        cmd = self.__keep_goal(bot)
        # print(cmd)
        self.__send_cmds.append(cmd)

    def __keep_goal(self, robot: Robot) -> RobotCommand:
        """keep_goal"""
        radian_ball_goal = radian_normalize(radian(self.__observer.ball, self.__our_goal))
        target_position = Point(
            self.__our_goal.x + self.__radius * math.cos(radian_ball_goal),
            self.__our_goal.y + self.__radius * math.sin(radian_ball_goal),
        )
        radian_target_robot = radian_normalize(radian(target_position, robot))
        speed = distance(target_position, robot) / 1000
        speed = min(speed, 1)

        command = RobotCommand(0)
        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_goal - robot.theta
        command.dribble_pow = 0
        command.kickpow = 0
        return command
