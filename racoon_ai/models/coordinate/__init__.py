#!/usr/bin/env python3.10

"""
    This module contains:
        - Point
        - Pose
        - Vector3f
"""

from dataclasses import dataclass, field


@dataclass()
class Point:
    """Point

    Attributes:
        x (float): The x coordinate
        y (float): The y coordinate
        z (float): The z coordinate
    """

    x: float
    y: float
    z: float = field(default=0)

    def __abs__(self) -> float:
        return float((self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Point") -> "Point":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other: "Point") -> "Point":
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self


@dataclass()
class Pose:
    """Pose

    Attributes:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float): The orientation of the pose in radians.
        z (float): The z-coordinate of the pose in millimeters.
    """

    x: float
    y: float
    theta: float = field(default=0)
    z: float = field(default=0)


@dataclass()
class Vector3f:
    """Vector3f

    Attributes:
        x (float): The x value
        y (float): The y value
        z (float): The z value
    """

    x: float
    y: float
    z: float = field(default=0)

    def __abs__(self) -> float:
        return float((self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5)

    def __add__(self, other: "Vector3f") -> "Vector3f":
        return Vector3f(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3f") -> "Vector3f":
        return Vector3f(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Vector3f") -> "Vector3f":
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other: "Vector3f") -> "Vector3f":
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def dot_prod(self, other: "Vector3f") -> float:
        """dot_prod

        Calculate the dot product

        Args:
            other (Vector3f): The other vector

        Returns:
            float: The dot product
        """
        return float(self.x * other.x + self.y * other.y + self.z * other.z)

    def cross_prod(self, other: "Vector3f") -> "Vector3f":
        """Cross product

        Calculate the cross product

        Args:
            other (Vector3f): The other vector

        Returns:
            Vector3f: The cross product
        """
        return Vector3f(
            self.y * other.z - self.z * other.y,
            -self.x * other.z + self.z * other.x,
            self.x * other.y - self.y * other.x,
        )
