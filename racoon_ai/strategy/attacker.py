#!/usr/bin/env python3.10

"""attacker.py

    This module is for the Attacker class.
"""

import math
from typing import TypeAlias

from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot.commands import RobotCommand
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


def radian(object1: RadFactors, object2: RadFactors) -> float:
    """radian

    Args:
        object1 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
        object2 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.

    Returns:
        float: degree of two objects in radian
    """
    return math.atan2(object1.y - object2.y, object1.x - object2.x)


def radian_normalize(rad: float) -> float:
    """radian_normalize

    Args:
        rad (float): radian value

    Returns:
        float: normalized radian value
    """
    if rad > math.pi:
        rad = rad - 2 * math.pi
    if rad < -math.pi:
        rad = rad + 2 * math.pi

    return rad


class Attacker:
    """Attacker

    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self, vision: VisionReceiver):
        self.__send_cmds: list[RobotCommand]
        self.__our_robots: list[SSL_DetectionRobot] = vision.blue_robots
        self.__ball: SSL_DetectionBall = vision.get_ball()

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def main(self) -> None:
        """main

        Returns:
            None
        """
        self.__send_cmds = []
        self.__send_cmds.append(self._straight_move_ball())

    def _straight_move_ball(self) -> RobotCommand:
        radian_ball_robot = radian_normalize(
            radian(self.__ball, self.__our_robots[0]) - self.__our_robots[0].orientation
        )

        command = RobotCommand(0)
        command.kickpow = 0
        command.vel_fwd = math.cos(radian_ball_robot)
        command.vel_sway = math.sin(radian_ball_robot)
        command.vel_angular = radian_ball_robot
        return command
