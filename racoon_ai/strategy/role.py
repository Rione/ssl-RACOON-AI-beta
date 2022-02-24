#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

import math
from typing import Any, TypeAlias


from racoon_ai.models.coordinate import Point
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


def distance(object1: RadFactors, object2: RadFactors) -> float:
    """distance

    Returns:
        float: distance value
    """
    return math.sqrt(math.pow(object1.x - object2.x, 2) + math.pow(object1.y - object2.y, 2))


class Role(object):
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
        self.__our_robots: list[SSL_DetectionRobot] = []
        self.__pass: int = 0
        self.__pass_receive: int = 0
        self.__keeper: int = 0
        self.__offense: list = []
        self.__defence: list = []
        self.__ball: SSL_DetectionBall
        self.__offense: Any
        self.__offense_quantity: int = 0
        self.__defence_quantity: int = 0

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__ball = vision.ball

    def decide_keeper(self) -> None:
        self.__keeper = 0

    def decide_role(self) -> None:
        """decide_role

        Returns:
            None
        """
        self.decide_keeper()

        self.__offense_quantity = 3
        self.__defence_quantity = 3

        self.decide_offense()
        self.decide_defence()
        print(self.__keeper)
        print(self.__offense)
        print(self.__defense)

    def decide_offense(self) -> None:
        offense = [[None for j in range(3)] for i in range(len(self.__our_robots))]
        for i in range(len(self.__our_robots)):
            offense[i][0] = i
            offense[i][1] = self.__our_robots[i].x
            offense[i][2] = self.__our_robots[i].y
        offense.sort(reverse=True, key=lambda x: x[1])
        offense = offense[:self.__offense_quantity]
        offense.sort(reverse=True, key=lambda x: x[2])
        self.__offense = [row[0] for row in offense]

    def decide_defence(self) -> None:
        defense = [[None for j in range(3)] for i in range(len(self.__our_robots)-1-self.__offense_quantity)]
        num = 0
        for i in range(len(self.__our_robots)):
            if i != self.__keeper and i not in self.__offense:
                defense[num][0] = i
                defense[num][1] = self.__our_robots[i].x
                defense[num][2] = self.__our_robots[i].y
                num += 1
        defense.sort(reverse=False, key=lambda x: x[1])
        defense = defense[:self.__defence_quantity]
        defense.sort(reverse=True, key=lambda x: x[2])
        self.__defense = [row[0] for row in defense]
