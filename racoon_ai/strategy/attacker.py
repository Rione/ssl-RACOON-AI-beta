#!/usr/bin/env python3.10

"""attacker.py

    This module is for the Attacker class.
"""

import math

from racoon_ai.models.official.grsim.commands import RobotCommand


def radian(object1, object2):
    if not (object1.x == object2.x):
        return math.atan2(object1.y - object2.y, object1.x - object2.x)
    else:
        return 0


def radian_normalize(rad):
    if rad > math.pi:
        rad = rad - 2 * math.pi
    if rad < -math.pi:
        rad = rad + 2 * math.pi

    return rad


class Attacker:
    def __init__(self, vision):
        self.__vision = vision
        self.__attacker_id = 0
        self.__kickspeedx = 0
        self.__kickspeedz = 0
        self.__veltangent = 0
        self.__velnormal = 0
        self.__velangular = 0
        self.__spinner = 0

        self.__our_robots = self.__vision.get_blue_robots()
        self.__balls = self.__vision.get_balls()

    def some_logics(self):
        pass

    def send_command(self):
        send_command = RobotCommand(
            self.__attacker_id,
            self.__kickspeedx,
            self.__kickspeedz,
            self.__veltangent,
            self.__velnormal,
            self.__velangular,
            self.__spinner,
            False,
            0,
            0,
            0,
            0,
        )
        return send_command

    def straight_move_ball(self):
        radian_ball_robot = radian_normalize(radian(self.__balls[0], self.__our_robots[0]) - self.__our_robots[0].theta)

        send_command = RobotCommand(
            self.__attacker_id,
            self.__kickspeedx,
            self.__kickspeedz,
            math.cos(radian_ball_robot),
            math.sin(radian_ball_robot),
            radian_ball_robot,
            self.__spinner,
            False,
            0,
            0,
            0,
            0,
        )
        return send_command
