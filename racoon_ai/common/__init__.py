#!/usr/bin/env python3.10
# pylint: disable=C0114

from math import atan2, cos, pi, sin, sqrt

from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand

MAX_SPEED = 1000.0
CLOSE_BALL = 150.0


def radian(pt1: Point, pt2: Point) -> float:
    """radian
    Args:
        pt1 Point: Calculatable object.
        pt2 Point: Calculatable object.
    Returns:
        float: degree of two objects in radian
    """
    return atan2(pt1.y - pt2.y, pt1.x - pt2.x)


def radian_normalize(rad: float) -> float:
    """radian_normalize

    Args:
        rad (float): radian value

    Returns:
        float: normalized radian value
    """
    if rad > pi:
        rad = rad - 2 * pi
    if rad < -pi:
        rad = rad + 2 * pi

    return rad


def distance(object1: Point, object2: Point) -> float:
    """distance

    Returns:
        float: distance value
    """
    return sqrt(pow(object1.x - object2.x, 2) + pow(object1.y - object2.y, 2))


def move2pose(robot: Robot, dist: Pose) -> RobotCommand:
    """move2pose

    Returns:
        RobotCommand: move motion value
    """
    command = RobotCommand(robot.robot_id)
    rotation = radian_normalize(dist.theta - robot.theta)
    radian_target_robot = radian_normalize(radian(dist, robot) - robot.theta)
    distance_target_robot = distance(dist, robot)

    speed = min(distance_target_robot / 100.0, MAX_SPEED)
    command.vel_fwd = cos(radian_target_robot) * speed
    command.vel_sway = sin(radian_target_robot) * speed
    command.vel_angular = radian_target_robot - rotation
    command.kickpow = 0.0
    command.dribble_pow = 0.0
    return command


def halt(robot: Robot) -> RobotCommand:
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
