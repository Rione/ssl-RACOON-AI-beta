#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

from typing import TypeAlias

from racoon_ai.common import distance
from racoon_ai.models.coordinate import Point
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


class SubRole:
    """SubRole
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
        self.__attacker: int = -1
        self.__receiver: int = -1
        self.__ball: SSL_DetectionBall

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__ball = vision.get_ball()

    def decide_sub_role(self) -> None:
        """decide_sub_role

        Returns:
            None
        """
        self.decide_attacker()
        self.decide_receiver()
        print(self.__attacker)
        print(self.__receiver)

    def decide_attacker(self) -> None:
        """decide_attacker

        Returns:
           None
        """
        attacker: list[list[float]] = []
        for robot in self.__our_robots:
            attacker.append([robot.robot_id, distance(self.__ball, robot)])
        attacker.sort(reverse=False, key=lambda x: x[1])
        self.__attacker = int(attacker[0][0])

    def decide_receiver(self) -> None:
        """decide_receiver

        Return:
          None
        """
        receiver: list[list[float]] = []
        for robot in self.__our_robots:
            if robot.robot_id != self.__attacker:
                receiver.append([robot.robot_id, distance(self.__ball, self.__our_robots[self.__attacker])])
        receiver.sort(reverse=False, key=lambda x: x[1])
        self.__receiver = int(receiver[0][0])
