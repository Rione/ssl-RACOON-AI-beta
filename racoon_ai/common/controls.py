#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

import math
from math import cos, sin

from numpy import array, dot, float64
from numpy.typing import NDArray

# from numpy import linalg as LA
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver


class Controls:
    """Keeper
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: MWReceiver) -> None:
        self.__pre_target_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__pre_robot_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__pre_target_theta: float = float(0)
        self.__pre_robot_theta: float = float(0)
        self.__target_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__accumulation: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__theta_accumulation: float = float(0)
        self.__dtaime: float = observer.sec_per_frame
        self.__k_gain: NDArray[float64] = array([8, 0.5, 1], dtype="float64")

    def pid(self, target: Pose, robot: Robot) -> RobotCommand:
        """pid"""
        cmd = RobotCommand(robot.robot_id)
        rbt: NDArray[float64] = array([robot.x / 1000, robot.y / 1000, robot.theta])
        self.__target_pose = array([target.x / 1000, target.y / 1000, target.theta])

        robot_speed = (rbt - self.__pre_robot_pose) / self.__dtaime
        target_speed = (self.__target_pose - self.__pre_target_pose) / self.__dtaime
        self.__accumulation += (self.__target_pose - rbt) * self.__dtaime
        # print(rbt - self.__pre_robot_pose)

        bbvel: NDArray[float64] = array([self.__target_pose - rbt, target_speed - robot_speed, self.__accumulation])

        bvel = dot(self.__k_gain, bbvel)

        transformation: NDArray[float64] = array(
            [
                [cos(robot.theta), -sin(robot.theta), 0],
                [sin(robot.theta), cos(robot.theta), 0],
                [0, 0, 1],
            ]
        )

        vel = dot(bvel, transformation)

        cmd.vel_angular = vel[2]
        if vel[0] * vel[0] + vel[1] * vel[1] > 1:
            vel /= math.sqrt(vel[0] * vel[0] + vel[1] * vel[1])
        cmd.vel_fwd = vel[0]
        cmd.vel_sway = vel[1]

        self.__pre_robot_pose = rbt
        self.__pre_target_pose = self.__target_pose

        return cmd

    def pid_radian(self, target_theta: float, robot: Robot) -> float:
        """pid_radian"""
        angular: float
        kp = self.__k_gain[0]
        kd = self.__k_gain[1]
        ki = self.__k_gain[2]
        e_robot = robot.theta - self.__pre_robot_theta
        e_target = target_theta - self.__pre_target_theta
        self.__theta_accumulation += (e_target - e_robot) * self.__dtaime
        angular = (
            kp * (target_theta - robot.theta)
            + kd * (e_target / self.__dtaime - e_robot / self.__dtaime)
            + ki * self.__theta_accumulation
        )

        self.__pre_target_theta = target_theta
        self.__pre_robot_theta = robot.theta

        angular = min(angular, math.pi)
        return angular
