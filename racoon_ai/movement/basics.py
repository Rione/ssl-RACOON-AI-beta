#!/usr/bin/env python3.10


"""basics.py

    This module contains:
        - move2pose
"""

from math import cos, sin

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand


def move2pose(robot: Robot, dist: Pose) -> RobotCommand:
    """move2pose

    Returns:
        RobotCommand: move motion value
    """
    command: RobotCommand = RobotCommand(robot.robot_id, use_imu=robot.is_imu_enabled)
    rotation: float = MU.radian_reduce(dist.theta, robot.theta)
    radian_target_robot: float = MU.radian_reduce(MU.radian(dist, robot), robot.theta)
    distance_target_robot: float = MU.distance(dist, robot)

    speed: float = min(distance_target_robot / 1000, 100)
    command.vel_fwd = cos(radian_target_robot) * speed
    command.vel_sway = sin(radian_target_robot) * speed
    command.vel_angular = MU.radian_reduce(radian_target_robot, rotation)
    command.target_pose = dist
    return command
