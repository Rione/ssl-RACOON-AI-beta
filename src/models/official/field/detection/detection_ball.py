#!/usr/bin/env python3.10

"""robot_custom_feedback.py

    This module contains the RobotCustomFeedback class.
"""

from models.official.field.pose_3_d import Pose3D


class DetectionBall(Pose3D):
    """DetectionBall

    A detection of a ball.

    Args:
        confidence (float): The confidence of the detection.
        area (float): The area of the detection.
        pixel_x (int): The x-coordinate of the detection in pixels.
        pixel_y (float): The y-coordinate of the detection in pixels.
        x (float): The x-coordinate of the detection in meters.
        y (float): The y-coordinate of the detection in meters.
        z (float): The z-coordinate of the detection in meters.
    """

    def __init__(
        self,
        confidence: float,
        area: int,
        pixel_x: float,
        pixel_y: float,
        x: float,
        y: float,
        z: float,
    ):

        self.__confidence: float = confidence

        self.__area: int = area

        self.__pixel_x: float = pixel_x

        self.__pixel_y: float = pixel_y

        Pose3D.__init__(self, x, y, z=z)

    def __str__(self):
        pass

    @property
    def confidence(self) -> float:
        """confidence

        Returns:
            float: The confidence of the detection.
        """
        return self.__confidence

    @property
    def area(self) -> int:
        """area

        Returns:
            int: The area of the detection.
        """
        return self.__area

    @property
    def pixel_x(self) -> float:
        """pixel_x

        Returns:
            float: The x-coordinate of the detection in pixels.
        """
        return self.__pixel_x

    @property
    def pixel_y(self) -> float:
        """pixel_y

        Returns:
            float: The y-coordinate of the detection in pixels.
        """
        return self.__pixel_y
