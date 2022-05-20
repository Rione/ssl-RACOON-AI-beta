#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

import math
from logging import getLogger

import numpy as np

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point
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
        self.__pre_target_point: Point = Point(0, 0)
        self.__pre_robot_position: Point = Point(0, 0)
        self.__accumulation: list[float] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.__target_theta: float = 0
        self.__target_point: Point = Point(0, 0)
        self.__pre_robot_theta: float = 0
        self.__pre_target_theta: float = 0

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
        self.__target_point = Point(
            self.__observer.goal.x + self.__radius * math.cos(radian_ball_goal),
            self.__observer.goal.y + self.__radius * math.sin(radian_ball_goal),
        )
        self.__target_theta = radian_ball_robot

        command = self.__pid_point(robot)
        command.vel_angular = self.__pid_radian(robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command

    def __pid_radian(self, robot: Robot) -> float:
        """pid_radian"""
        kp = 5
        kd = 1
        ki = 10
        e_robot = robot.theta - self.__pre_robot_theta
        e_target = self.__target_theta - self.__pre_target_theta
        self.__accumulation[3] += e_robot * 0.016
        self.__accumulation[6] += e_target * 0.016
        # print(round((self.__target_theta - robot.theta), 0))
        angular = (
            kp * (self.__target_theta - robot.theta)
            + kd * (e_target / 0.016 - e_robot / 0.016)
            + ki * (self.__accumulation[6] - self.__accumulation[3])
        )
        angular = min(angular, math.pi)

        self.__pre_target_theta = self.__target_theta
        self.__pre_robot_theta = robot.theta
        return angular

    def __pid_point(self, robot: Robot) -> RobotCommand:
        """pid_point"""
        e_robot: Point
        e_target: Point
        bvel: list[list[float]]
        cmd = RobotCommand(robot.robot_id)
        kp = 10 / 1000
        kd = 1 / 1000
        ki = 20 / 1000
        e_robot = robot - self.__pre_robot_position
        e_target = self.__target_point - self.__pre_target_point
        self.__accumulation[1] += e_robot.x * 0.016
        self.__accumulation[2] += e_robot.y * 0.016
        self.__accumulation[4] += e_target.x * 0.016
        self.__accumulation[5] += e_target.y * 0.016

        bvel = [
            [
                kp * (self.__target_point.x - robot.x)
                + kd * (e_target.x / 0.016 - e_robot.x / 0.016)
                + ki * (self.__accumulation[4] - self.__accumulation[1])
            ],
            [
                kp * (self.__target_point.y - robot.y)
                + kd * (e_target.y / 0.016 - e_robot.y / 0.016)
                + ki * (self.__accumulation[5] - self.__accumulation[2])
            ],
        ]
        transformation = [
            [math.cos(robot.theta), math.sin(robot.theta)],
            [-math.sin(robot.theta), math.cos(robot.theta)],
        ]
        vel = np.dot(transformation, bvel)
        if vel[0, 0] * vel[0, 0] + vel[1, 0] * vel[1, 0] > 1:
            vel /= math.sqrt(vel[0, 0] * vel[0, 0] + vel[1, 0] * vel[1, 0])
        cmd.vel_fwd = vel[0, 0]
        cmd.vel_sway = vel[1, 0]

        self.__pre_robot_position = Point(robot.x, robot.y)
        self.__pre_target_point = Point(self.__target_point.x, self.__target_point.y)

        return cmd
