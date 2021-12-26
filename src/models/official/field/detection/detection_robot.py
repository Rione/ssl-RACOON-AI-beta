#!/usr/bin/env python3.10

"""robot_custom_feedback.py

    This module contains the DetectionRobot class.
"""

from models.official.field.pose_2_d import Pose2D
from models.official.field.robot_controll.robot_feedback import RobotFeedback


class DetectionRobot(RobotFeedback, Pose2D):
    """DetectionRobot

    A detection of a robot.

    Args:
        confidence (float): The confidence of the detection.
        robot_id (int): The id of the robot.
        x (float): The x-coordinate of the robot in millimeters.
        y (float): The y-coordinate of the robot in millimeters.
        theta (float): The orientation of the robot in radians.
        pixel_x (float): The x-coordinate of the robot in pixels.
        pixel_y (float): The y-coordinate of the robot in pixels.
        height (float): The height of the robot in millimeters.
    """

    def __init__(
        self,
        confidence: float,
        robot_id: int,
        x: float,
        y: float,
        theta: float,
        pixel_x: float,
        pixel_y: float,
        height: float,
    ):

        self.__confidence: float = confidence

        self.__robot_id: int = robot_id

        self.__pixel_x: float = pixel_x

        self.__pixel_y: float = pixel_y

        self.__height: float = height

        Pose2D.__init__(self, x, y, theta)

    def __str__(self) -> str:
        pass

    @property
    def confidence(self):
        """confidence

        Returns:
            float: The confidence of the detection.
        """
        return self.__confidence

    @property
    def robot_id(self) -> int:
        """robot_id

        Returns:
            int: The id of the robot.
        """
        return self.__robot_id

    @property
    def pixel_x(self) -> float:
        """pixel_x

        Returns:
            float: The x-coordinate of the robot in pixels.
        """
        return self.__pixel_x

    @property
    def pixel_y(self) -> float:
        """pixel_y

        Returns:
            float: The y-coordinate of the robot in pixels.
        """
        return self.__pixel_y

    @property
    def height(self) -> float:
        """height

        Returns:
            float: The height of the robot in millimeters.
        """
        return self.__height
