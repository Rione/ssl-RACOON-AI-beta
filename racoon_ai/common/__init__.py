#!/usr/bin/env python3.10
# pylint: disable=C0114

import math
from typing import TypeAlias

from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot.commands import RobotCommand
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot
MAX_SPEED = 1000.0
CLOSE_BALL = 150.0


def radian(object1: RadFactors, object2: RadFactors) -> float:
    """radian
    Args:
        object1 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
        object2 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
    Returns:
        float: degree of two objects in radian
    """
    return math.atan2(object1.y - object2.y, object1.x - object2.x)


def sub_radian(object1: RadFactors, object2: RadFactors) -> float:
    """sub_radian
    Args:
        object1 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
        object2 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
    Returns:
        float: degree of two objects in radian (not atan2)
    """
    return math.atan((object1.y - object2.y) / (object1.x - object2.x))


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


def distance(object1: RadFactors, object2: RadFactors) -> float:
    """distance

    Returns:
        float: distance value
    """
    return math.sqrt(math.pow(object1.x - object2.x, 2) + math.pow(object1.y - object2.y, 2))


def move_point(robot: SSL_DetectionRobot, target_angular: RadFactors, target_position: RadFactors) -> RobotCommand:
    """move_point

    Returns:
        RobotCommand: move motion value
    """
    command = RobotCommand(robot.robot_id)
    radian_angular_target_robot = radian_normalize(radian(target_angular, robot) - robot.orientation)
    radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
    distance_target_robot = distance(target_position, robot)

    speed = distance_target_robot / 1000.0
    speed = min(speed, MAX_SPEED)

    command.vel_fwd = math.cos(radian_target_robot) * speed
    command.vel_sway = math.sin(radian_target_robot) * speed
    command.vel_angular = radian_angular_target_robot
    command.kickpow = 0.0
    command.dribble_pow = 0.0
    return command


def halt(robot: SSL_DetectionRobot) -> RobotCommand:
    """halt

    Returns:
        RobotCommand: halt value
    """
    command = RobotCommand(robot.robot_id)
    command.vel_fwd = 0.0
    command.vel_sway = 0.0
    command.vel_angular = 0.0
    command.kickpow = 0.0
    command.dribble_pow = 0.0

    return command
