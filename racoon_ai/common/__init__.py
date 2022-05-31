#!/usr/bin/env python3.10
# pylint: disable=C0114

from math import cos, sin
from typing import TypeAlias

from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand

from .math_utils import MathUtils

MAX_SPEED: float = 1000.0
CLOSE_BALL: float = 150.0
MU: TypeAlias = MathUtils


def move2pose(robot: Robot, dist: Pose) -> RobotCommand:
    """move2pose

    Returns:
        RobotCommand: move motion value
    """
    command = RobotCommand(robot.robot_id)
    rotation = MU.radian_reduce(dist.theta, robot.theta)
    radian_target_robot = MU.radian_reduce(MU.radian(dist, robot), robot.theta)
    distance_target_robot = MU.distance(dist, robot)

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


__all__ = [
    "MathUtils",
    "CLOSE_BALL",
    "MAX_SPEED",
    "move2pose",
    "halt",
]
