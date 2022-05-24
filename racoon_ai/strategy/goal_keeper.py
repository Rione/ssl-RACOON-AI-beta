#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

import math
from logging import getLogger
from math import cos, sin

from numpy import array, dot, float64
from numpy.typing import NDArray

# from numpy import linalg as LA
from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver


class Keeper:
    """Keeper
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
        self.__radius: float = 750
        self.__pre_target_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__pre_robot_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__target_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__accumulation: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__dtaime: float = observer.sec_per_frame
        self.__k_gain: NDArray[float64] = array([8, 0.5, 1], dtype="float64")

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
        radian_ball_goal = MU.radian(self.__observer.ball, self.__observer.goal)
        radian_ball_robot = MU.radian(self.__observer.ball, robot)

        if abs(radian_ball_goal) >= math.pi / 2:
            radian_ball_goal = radian_ball_goal / abs(radian_ball_goal) * math.pi / 2
        self.__target_pose = array(
            [
                (self.__observer.goal.x + self.__radius * cos(radian_ball_goal)) / 1000,
                (self.__observer.goal.y + self.__radius * sin(radian_ball_goal)) / 1000,
                radian_ball_robot,
            ]
        )

        command = self.__pid(robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command

    def __pid(self, robot: Robot) -> RobotCommand:
        """pid"""
        cmd = RobotCommand(robot.robot_id)

        rbt: NDArray[float64] = array([robot.x / 1000, robot.y / 1000, robot.theta])
        robot_speed = (rbt - self.__pre_robot_pose) / self.__dtaime
        target_speed = (self.__target_pose - self.__pre_target_pose) / self.__dtaime
        self.__accumulation += (self.__target_pose - rbt) * self.__dtaime
        print(rbt - self.__pre_robot_pose)

        bbvel: NDArray[float64] = array([self.__target_pose - rbt, target_speed - robot_speed, self.__accumulation])

        bvel = dot(self.__k_gain, bbvel)

        transformation: NDArray[float64] = array(
            [
                [cos(robot.theta), -sin(robot.theta), 0],
                [sin(robot.theta), cos(robot.theta), 0],
                [0, 0, 1],
            ]
        )

        vel = dot(bvel, transformation)

        cmd.vel_angular = vel[2]
        if vel[0] * vel[0] + vel[1] * vel[1] > 1:
            vel /= math.sqrt(vel[0] * vel[0] + vel[1] * vel[1])
        cmd.vel_fwd = vel[0]
        cmd.vel_sway = vel[1]

        self.__pre_robot_pose = rbt
        self.__pre_target_pose = self.__target_pose

        return cmd
