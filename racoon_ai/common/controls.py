#!/usr/bin/env python3.10

"""goal_keeper.py

    This module is for the Keeper class.
"""

from logging import getLogger
from math import cos, pi, sin
from typing import Tuple

from numpy import array, divide, dot, float64, multiply, subtract
from numpy.linalg import norm
from numpy.typing import NDArray

# from numpy import linalg as LA
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver


class Controls:
    """Controls
    Args:
        observer (Observer): Observer instance
        k_gain (Tuple[float, float, float]): PID gain

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: MWReceiver, k_gain: Tuple[float, float, float] = (8, 0.5, 1)) -> None:
        self.__logger = getLogger(__name__)
        self.__pre_target_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__pre_bot_pose: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__accumulations: NDArray[float64] = array([0, 0, 0], dtype="float64")
        self.__k_gain: NDArray[float64] = array(k_gain, dtype="float64")
        self.__dtaime: float = observer.sec_per_frame
        self.__pre_target_theta: float = float(0)
        self.__pre_bot_theta: float = float(0)
        self.__theta_accumulation: float = float(0)

    def pid(self, target: Pose, bot: Robot) -> RobotCommand:
        """pid

        Args:
            target (Pose): Target pose
            bot (Robot): Robot instance

        Returns:
            RobotCommand: RobotCommand instance
        """
        cmd = RobotCommand(bot.robot_id)
        bot_pose: NDArray[float64] = array([bot.x / 1000, bot.y / 1000, bot.theta])
        target_pose: NDArray[float64] = array([target.x / 1000, target.y / 1000, target.theta])

        bot_speed: NDArray[float64] = divide(subtract(bot_pose, self.__pre_bot_pose), self.__dtaime)
        target_speed: NDArray[float64] = divide(subtract(target_pose, self.__pre_target_pose), self.__dtaime)

        diff_pose: NDArray[float64] = subtract(target_pose, bot_pose)
        diff_speed: NDArray[float64] = subtract(target_speed, bot_speed)

        self.__accumulations += multiply(diff_pose, self.__dtaime)
        self.__logger.debug("accumulation: %s", self.__accumulations)

        bbvel: NDArray[float64] = array([diff_pose, diff_speed, self.__accumulations])
        bvel: NDArray[float64] = dot(self.__k_gain, bbvel)

        local_pose: NDArray[float64] = array(
            [
                [cos(bot.theta), -sin(bot.theta), 0],
                [sin(bot.theta), cos(bot.theta), 0],
                [0, 0, 1],
            ]
        )

        vel: NDArray[float64] = dot(bvel, local_pose)
        abs_vel_xy = norm(vel[:2].transpose())  # Convert into [x, y], and get the norm
        if (abs_vel_xy**2) > 1:
            divide(vel, abs_vel_xy, vel)

        cmd.vel_fwd = float(vel[0])
        cmd.vel_sway = float(vel[1])
        cmd.vel_angular = float(vel[2])

        self.__pre_bot_pose = bot_pose
        self.__pre_target_pose = target_pose

        return cmd

    def pid_radian(self, target_theta: float, bot: Robot) -> float:
        """pid_radian

        Args:
            target_theta (float): Target theta
            bot (Robot): Robot instance
        """
        vel_angular: float = float(0)
        kp: float = float(self.__k_gain[0])
        kd: float = float(self.__k_gain[1])
        ki: float = float(self.__k_gain[2])

        e_bot: float = bot.theta - self.__pre_bot_theta
        e_target: float = target_theta - self.__pre_target_theta
        self.__theta_accumulation += (e_target - e_bot) * self.__dtaime

        vel_angular += kp * (target_theta - bot.theta)
        vel_angular += kd * ((e_target / self.__dtaime) - (e_bot / self.__dtaime))
        vel_angular += ki * self.__theta_accumulation

        self.__pre_target_theta = target_theta
        self.__pre_bot_theta = bot.theta

        vel_angular = min(vel_angular, pi)
        return vel_angular
