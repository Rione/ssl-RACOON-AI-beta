#!/usr/bin/env python3.10

"""pose_3_d.py

    This module contains the Pose3D class.
"""

from models.official.field.pose_2_d import Pose2D


class Pose3D(Pose2D):
    """Pose3D

    Args:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float, optional): The orientation of the pose in radians. Defaults to 0.
        z (float, optional): The z-coordinate of the pose in millimeters. Defaults to 0.
    """

    def __init__(self, x: float, y: float, theta: float = 0, z: float = 0):

        # [mm]
        self.__z: float = z

        super().__init__(x, y, theta)

    def __str__(self) -> str:
        pass

    @property
    def z(self) -> float:
        """z

        Returns:
            float: The z-coordinate of the pose in millimeters.
        """
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        """z

        Args:
            value (float): The z-coordinate of the pose in millimeters.
        """
        self.__z = value
