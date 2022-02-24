#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

import math
from typing import Any, TypeAlias

from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.models.coordinate import Point
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


class SubRole(object):
    """Observer
    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self) -> None:
        self.__our_robots: list[SSL_DetectionRobot]
        self.__pass: int = 0
        self.__pass_receive: int = 0
        self.__ball: SSL_DetectionBall
        self.__offense: Any

    def vision_receive(self, vision: VisionReceiver, offense: Any) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__ball = vision.ball

        self.__offense = offense

    def _decide_pass(self) -> None:
        if self.__offense.get_kick_flag() is False:
            min_distance = 10000000.0
            self.__pass = -1
            for robot in self.__our_robots:
                distance_robot_ball = distance(robot, self.__ball)
                if distance_robot_ball < min_distance:
                    min_distance = distance_robot_ball
                    self.__pass = robot.robot_id

    def _decide_pass_receive(self) -> None:
        if self.__pass == 1:
            self.__pass_receive = 0
        else:
            self.__pass_receive = 1

    def decide_role(self) -> None:
        """decide_role

        Returns:
            None
        """
        self._decide_pass()
        self._decide_pass_receive()

    def get_pass(self) -> int:
        """get_pass

        Returns:
            int
        """
        return self.__pass

    def get_pass_receive(self) -> int:
        """get_pass_receive

        Returns:
            int
        """
        return self.__pass_receive
