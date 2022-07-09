#!/usr/bin/env python3.10


"""basics.py

    This module contains:
        - move2pose
"""

from math import cos, sin

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand


def halt_all(target_ids: set[int], *, look_at_reference_dir: bool = True) -> list[RobotCommand]:
    """halt_all

    Args:
        target_ids (set[int]): Target IDs.
        look_at_reference_dir (bool, optional): Look at reference direction (default: True).

    Returns:
        list[RobotCommand]: halt command
    """
    return [RobotCommand(i) for i in ({255} if not look_at_reference_dir else target_ids)]


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


def _reset_imu(bot: Robot) -> RobotCommand:
    """reset_imu

    Args:
        bot (Robot)

    Returns:
        RobotCommand
    """
    cmd: RobotCommand = RobotCommand(bot.robot_id + 100, use_imu=bot.is_imu_enabled)
    cmd.target_pose = bot
    return cmd


def reset_all_imu(our_available_bots: set[Robot]) -> list[RobotCommand]:
    """reset_all_imu

    Args:
        target_ids (set[int])

    Returns:
        list[RobotCommand]
    """
    return list(map(_reset_imu, (bot for bot in our_available_bots if bot.is_imu_enabled)))
