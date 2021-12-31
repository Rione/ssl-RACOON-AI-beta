#!/usr/bin/env python3.10

"""coordinate.py

    This module contains:
        - Orientation
        - Pose2D
        - Pose3D
"""

from racoon_ai.models.official.vision.detection_tracked import Vector2f, Vector3f


class Orientation:
    """Pose

    Attributes:
        theta (float): orientation in radians
    """

    def __init__(self, theta: float) -> None:
        self.__theta: float = theta

    @property
    def theta(self) -> float:
        """theta

        Returns:
            float: theta value
        """
        return self.__theta

    @theta.setter
    def theta(self, value: float) -> None:
        """theta

        Args:
            value (float): theta value
        """
        self.__theta = value


class Pose2D(Vector2f, Orientation):
    """Pose2D

    Attributes:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float, optional): The orientation of the pose in radians. Defaults to 0.
    """

    def __init__(self, x: float, y: float, theta: float = 0) -> None:
        Vector2f.__init__(self, x, y)
        Orientation.__init__(self, theta)

    def __str__(self) -> str:
        return "Pose2D(" f"x={self.x:.2f}, " f"y={self.y:.2f}, " f"theta={self.theta:.2f}" ")"

    def __repr__(self) -> str:
        return f"Pose2D({self.x}, {self.y}, {self.theta})"

    def __iadd__(self, other: object) -> "Pose2D":
        raise NotImplementedError

    def __isub__(self, other: object) -> "Pose2D":
        raise NotImplementedError

    def __add__(self, other: object) -> "Pose2D":
        raise NotImplementedError

    def __sub__(self, other: object) -> "Pose2D":
        raise NotImplementedError

    def __abs__(self) -> float:
        raise NotImplementedError


class Pose3D(Vector3f, Orientation):
    """Pose3D

    Attributes:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float, optional): The orientation of the pose in radians. Defaults to 0.
        z (float, optional): The z-coordinate of the pose in millimeters. Defaults to 0.
    """

    def __init__(self, x: float, y: float, theta: float = 0, z: float = 0):
        Vector3f.__init__(self, x, y, z)
        Orientation.__init__(self, theta)

    def __str__(self) -> str:
        return "Pose3D(" f"x={self.x:.2f}, " f"y={self.y:.2f}, " f"theta={self.theta:.2f}, " f"z={self.z:.2f}" ")"

    def __repr__(self) -> str:
        return f"Pose3D({self.x}, {self.y}, {self.theta}, {self.z})"

    def __iadd__(self, other: object) -> "Pose3D":
        raise NotImplementedError

    def __isub__(self, other: object) -> "Pose3D":
        raise NotImplementedError

    def __add__(self, other: object) -> "Pose3D":
        raise NotImplementedError

    def __sub__(self, other: object) -> "Pose3D":
        raise NotImplementedError

    def __abs__(self) -> float:
        raise NotImplementedError


if __name__ == "__main__":
    vc2f = Vector2f(1, 2)
    vc2f += Vector2f(3, 4)
    print(vc2f)
    vc2f -= Vector2f(3, 4)
    print(f"{vc2f == Vector2f(1, 2) = }")
    print(vc2f > Vector2f(3, 4))
    print(vc2f >= Vector2f(3, 4))
    print(vc2f == Vector2f(1, 2))
    print(vc2f != Vector2f(1, 2))
    print(vc2f < Vector2f(3, 4))
    print(vc2f <= Vector2f(1, 1.9))

    print()

    vc3f = Vector3f(1, 2, 3)
    vc3f += Vector3f(3, 4, 5)
    print(f"{vc3f = }")
    vc3f -= Vector3f(3, 4, 5)
    print(f"{vc3f == Vector3f(1, 2, 3) = }")
    print(f"{vc3f > Vector3f(3, 4, 5) = }")
    print(f"{vc3f >= Vector3f(3, 4, 5) = }")
    print(f"{vc3f == Vector3f(1, 2, 3) = }")
    print(f"{vc3f != Vector3f(1, 2, 3) = }")
    print(f"{vc3f < Vector3f(3, 4, 5) = }")
    print(f"{vc3f <= Vector3f(3, 4, 5) = }")

    print()

    pose2d = eval(repr(Pose2D(1, 2, 3)))
    print(f"{pose2d = }")
    print(pose2d)

    print()

    pose3d = eval(repr(Pose3D(1, 2, 3, 4)))
    print(f"{pose3d = }")
    print(pose3d)
