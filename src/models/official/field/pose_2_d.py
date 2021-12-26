#!/usr/bin/env python3.10

"""pose_2_d.py

    This module contains the Pose2D class.
"""

from models.official.field.geometry.vector_2_f import Vector2f


class Pose2D(Vector2f):
    """Pose2D

    Args:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float, optional): The orientation of the pose in radians. Defaults to 0.
    """

    def __init__(self, x: float, y: float, theta: float = 0):

        # [rad]
        self.__theta: float = theta

        super().__init__(x, y)

    def __str__(self) -> str:
        pass

    @property
    def theta(self) -> float:
        """theta

        Returns:
            float: The orientation of the pose in radians.
        """
        return self.__theta

    @theta.setter
    def theta(self, value: float) -> None:
        """theta

        Args:
            value (float): The orientation of the pose in radians.
        """
        self.__theta = value
