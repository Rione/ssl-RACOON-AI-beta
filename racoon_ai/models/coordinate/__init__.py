#!/usr/bin/env python3.10

"""
    This module contains:
        - Point
        - Pose
"""

from dataclasses import dataclass, field


@dataclass()
class Point:
    """Point

    Attributes:
        x (float): The x coordinate.
        y (float): The y coordinate.
        z (float): The z coordinate.
    """

    x: float
    y: float
    z: float = field(default=0)

    def __abs__(self) -> float:
        return float((self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5)

    def __add__(self, other: "Point") -> "Point":
        """Add two points"""
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        """Subtract two points"""
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __iadd__(self, other: "Point") -> "Point":
        """Add two points"""
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other: "Point") -> "Point":
        """Subtract two points"""
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
