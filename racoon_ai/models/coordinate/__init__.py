#!/usr/bin/env python3.10

"""
    This module contains:
        - Point
        - Pose
        - Vector3f
"""


class Point:
    """Point

    Attributes:
        x (float): The x coordinate
        y (float): The y coordinate
        z (float): The z coordinate
    """

    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.__x: float = x
        self.__y: float = y
        self.__z: float = z

    def __str__(self) -> str:
        return f"(x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Point):
            return False
        return (self.x == obj.x) and (self.y == obj.y) and (self.z == obj.z)

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

    @property
    def x(self) -> float:
        """x"""
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @property
    def y(self) -> float:
        """y"""
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    @property
    def z(self) -> float:
        """z"""
        return self.__z

    @z.setter
    def z(self, z: float) -> None:
        self.__z = z


class Pose(Point):
    """Pose

    Attributes:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float): The orientation of the pose in radians.
        z (float): The z-coordinate of the pose in millimeters.
    """

    def __init__(self, x: float, y: float, theta: float = 0, z: float = 0) -> None:
        super().__init__(x, y, z)
        self.__theta: float = theta

    def __str__(self) -> str:
        return f"(x={self.x:.1f}, y={self.y:.1f}, theta={self.theta:.1f}, z={self.z:.1f})"

    def __repr__(self) -> str:
        return f"Pose({self.x}, {self.y}, {self.theta}, {self.z})"

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Pose):
            return False
        return (self.x == obj.x) and (self.y == obj.y) and (self.z == obj.z) and (self.theta == obj.theta)

    @property
    def theta(self) -> float:
        """theta"""
        return self.__theta

    @theta.setter
    def theta(self, theta: float) -> None:
        self.__theta = theta


class Vector3f:
    """Vector3f

    Attributes:s
        x (float): The x value
        y (float): The y value
        z (float): The z value
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.__x: float = x
        self.__y: float = y
        self.__z: float = z

    def __str__(self) -> str:
        return f"({self.x:.1f}, {self.y:.1f}, {self.z:.1f})"

    def __repr__(self) -> str:
        return f"Vector3f({self.x}, {self.y}, {self.z})"

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

    @property
    def x(self) -> float:
        """x"""
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @property
    def y(self) -> float:
        """y"""
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    @property
    def z(self) -> float:
        """z"""
        return self.__z

    @z.setter
    def z(self, z: float) -> None:
        self.__z = z

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
