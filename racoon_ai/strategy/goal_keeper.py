#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

from logging import getLogger
from math import cos, sin

from click import command

from racoon_ai.common import Controls
from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver


class Keeper:
    """Keeper
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: MWReceiver, controls: Controls) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")
        self.__observer = observer
        self.__controls = controls
        # self.__role = role
        self.__send_cmds: list[RobotCommand]
        self.__radius: float = 750

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

        bot = self.__observer.our_robots[0]
        cmd = self.__keep_goal(bot)
        self.__send_cmds.append(cmd)

    def __keep_goal(self, robot: Robot) -> RobotCommand:
        """keep_goal"""
        # radian_ball_goal = MU.radian(self.__observer.ball, self.__observer.goal)
        # radian_ball_robot = MU.radian(self.__observer.ball, robot)

        # if abs(radian_ball_goal) >= MU.PI / 2:
        #     radian_ball_goal = ((radian_ball_goal / abs(radian_ball_goal)) * MU.PI) / 2
        # target_pose = Pose(
        #     (self.__observer.goal.x + self.__radius * cos(radian_ball_goal)),
        #     (self.__observer.goal.y + self.__radius * sin(radian_ball_goal)),
        #     radian_ball_robot,
        # )

        # command = self.__controls.pid(target_pose, robot)
        # command.vel_fwd = 1
        command.dribble_pow = 0
        command.kickpow = 0
        return command
