#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

import math
from logging import getLogger
from typing import Any

from racoon_ai.common import distance, move_point, radian, radian_normalize
from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot import RobotCommand
from racoon_ai.networks import VisionReceiver
from racoon_ai.observer.observer import Observer
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot


class Offense:
    """Offense
    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self, observer: Observer, role: Any):
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        self.__role: Any = role
        self.__send_cmds: list[RobotCommand]
        self.__our_robots: list[SSL_DetectionRobot]
        self.__ball: SSL_DetectionBall
        # self.__their_robots: list[SSL_DetectionRobot]
        self.__kick_flag: bool = False
        # self.__arrive_flag: bool = False

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__ball = vision.get_ball()
        # self.__their_robots = vision.yellow_robots

    def main(self) -> None:
        """main

        Returns:
            None
        """
        # commandの情報を格納するリスト
        self.__send_cmds = []

        # 一番ボールに近いロボットがボールに向かって前進
        self.__send_cmds.append(self._straight_move_ball(self.__our_robots[0]))

        # (x,y)=(2000,2000)の地点に１番ロボットを移動させる
        target_position = Point(2000, 2000, 0)
        print(self.__our_robots)
        self.__send_cmds.append(move_point(self.__our_robots[1], self.__ball, target_position))

    def _pass_receive(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        target_position = Point(0, 0, 0)
        distance_ball_robot = distance(self.__our_robots[robot.robot_id], self.__ball)

        if distance_ball_robot < 150:
            self.__kick_flag = False

        if self.__kick_flag is True and self.__observer.get_ball_slope() != 0:
            target_position.x = (
                robot.y - self.__observer.get_ball_intercept() - (-1 / self.__observer.get_ball_slope()) * robot.x
            ) / (self.__observer.get_ball_slope() - (-1 / self.__observer.get_ball_slope()))
            target_position.y = (
                self.__observer.get_ball_slope() * target_position.x + self.__observer.get_ball_intercept()
            )
        angular = radian_normalize(radian(self.__ball, robot) - robot.orientation)

        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_target_robot = distance(target_position, robot)
        speed = distance_target_robot / 1000

        fwd = math.cos(radian_target_robot) * speed
        sway = math.sin(radian_target_robot) * speed

        command.vel_fwd = fwd
        command.vel_sway = sway
        command.vel_angular = angular
        command.dribble_pow = 1
        command.kickpow = 0

        return command

    def _straight_move_ball(self, robot: SSL_DetectionRobot) -> RobotCommand:
        radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        distance_target_robot = distance(self.__ball, robot)
        speed = distance_target_robot / 1000.0

        dribble_power = 0.0
        # スピード制限
        if speed >= 1.0:
            speed = 1.0
        else:
            dribble_power = 1.0

        command = RobotCommand(robot.robot_id)
        command.vel_fwd = math.cos(radian_ball_robot) * speed
        command.vel_sway = math.sin(radian_ball_robot) * speed
        command.vel_angular = radian_ball_robot
        command.dribble_pow = dribble_power
        command.kickpow = 0
        return command

    def get_kick_flag(self) -> bool:
        """
        Returns:
            bool: __kick_flag
        """
        return self.__kick_flag
