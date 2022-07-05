#!/usr/bin/env python3.10

"""
    This module contains:
        - Point
        - Pose
        - Vector3f
"""

from numpy import array, float32
from numpy.typing import NDArray


class Point:
    """Point

    Attributes:
        x (float): The x coordinate
        y (float): The y coordinate
        z (float, optional): The z coordinate

    Examples:
        Specifying the 2D point (x, and y):
        >>> Point(1, 2)
        Point(1.0, 2.0, 0.0)

        Specifying the 3D point (x, y, and z):
        >>> Point(1, 2, 3)
        Point(1.0, 2.0, 3.0)
    """

    def __init__(self, x: float, y: float, z: float = 0) -> None:
        self.__x: float = float(x)
        self.__y: float = float(y)
        self.__z: float = float(z)

    def __str__(self) -> str:
        return f"(x={self.x:.1E}, y={self.y:.1E}, z={self.z:.1E})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Point):
            return False
        return (self.x == obj.x) and (self.y == obj.y) and (self.z == obj.z)

    def __abs__(self) -> float:
        return float((self.x**2 + self.y**2 + self.z**2) ** 0.5)

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
        self.__x = float(x)

    @property
    def y(self) -> float:
        """y"""
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = float(y)

    @property
    def z(self) -> float:
        """z"""
        return self.__z

    @z.setter
    def z(self, z: float) -> None:
        self.__z = float(z)

    @staticmethod
    def from_vector3f(obj: "Vector3f") -> "Point":
        """from_vector3f

        Args:
            obj (Vector3f): The vector3f to convert

        Returns:
            Point: The converted point

        Examples:
            >>> Point.from_vector3f(Vector3f(1, 2, 3))
            Point(1.0, 2.0, 3.0)
        """
        return Point(obj.x, obj.y, z=obj.z)


class Pose(Point):
    """Pose

    Attributes:
        x (float): The x-coordinate of the pose in millimeters.
        y (float): The y-coordinate of the pose in millimeters.
        theta (float, optional): The orientation of the pose in radians.
        z (float, optional): The z-coordinate of the pose in millimeters.

    Examples:
        Specifying the 2D Point:
        >>> Pose(1, 2)
        Pose(1.0, 2.0, 0.0, 0.0)

        Specifying the orientation:
        >>> Pose(1, 2, 3)
        Pose(1.0, 2.0, 3.0, 0.0)

        Specifying the 3D Pose:
        >>> Pose(1, 2, 3, 4)
        Pose(1.0, 2.0, 3.0, 4.0)
    """

    def __init__(self, x: float, y: float, theta: float = 0, z: float = 0) -> None:
        super().__init__(x, y, z)
        self.__theta: float = float(theta)

    def __str__(self) -> str:
        return f"(x={self.x:.1E}, y={self.y:.1E}, theta={self.theta:.1E}, z={self.z:.1E})"

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
        self.__theta = float(theta)

    @staticmethod
    def from_point(obj: Point) -> "Pose":
        """from_point

        Args:
            obj (Point): The point to convert

        Returns:
            Pose: The converted pose

        Examples:
            >>> Pose.from_point(Point(1, 2, 3))
            Pose(1.0, 2.0, 0.0, 3.0)
        """
        return Pose(obj.x, obj.y, theta=0, z=obj.z)

    @staticmethod
    def from_vector3f(obj: "Vector3f") -> "Pose":
        """from_vector3f

        Args:
            obj (Vector3f): The vector3f to convert

        Returns:
            Pose: The converted pose

        Examples:
            >>> Pose.from_vector3f(Vector3f(1, 2, 3))
            Pose(1.0, 2.0, 0.0, 3.0)
        """
        return Pose(obj.x, obj.y, z=obj.z)


class Vector3f:
    """Vector3f

    Attributes:s
        x (float): The x value
        y (float): The y value
        z (float): The z value
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.__x: float = float(x)
        self.__y: float = float(y)
        self.__z: float = float(z)

    def __str__(self) -> str:
        return f"({self.x:.1E}, {self.y:.1E}, {self.z:.1E})"

    def __repr__(self) -> str:
        return f"Vector3f({self.x}, {self.y}, {self.z})"

    def __abs__(self) -> float:
        return float((self.x**2 + self.y**2 + self.z**2) ** 0.5)

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
        self.__x = float(x)

    @property
    def y(self) -> float:
        """y"""
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        self.__y = float(y)

    @property
    def z(self) -> float:
        """z"""
        return self.__z

    @z.setter
    def z(self, z: float) -> None:
        self.__z = float(z)

    @staticmethod
    def from_point(obj: Point) -> "Vector3f":
        """from_point

        Args:
            obj (Point): The point to convert

        Returns:
            Vector3f: The converted vector3f

        Examples:
            >>> Vector3f.from_point(Point(1, 2, 3))
            Vector3f(1.0, 2.0, 3.0)
        """
        return Vector3f(obj.x, obj.y, obj.z)

    @staticmethod
    def from_pose(obj: Pose) -> "Vector3f":
        """from_pose

        Args:
            obj (Pose): The pose to convert

        Returns:
            Vector3f: The converted vector3f

        Examples:
            >>> Vector3f.from_pose(Pose(1, 2, 3))  # NOTE: Pose is in order of (x, y, theta, z)
            Vector3f(1.0, 2.0, 0.0)
        """
        return Vector3f(obj.x, obj.y, obj.z)

    def to_np_array(self) -> NDArray[float32]:
        """to_np_array

        Returns:
            np.ndarray: The converted numpy array

        Examples:
            >>> Vector3f.from_pose(Pose(1, 2, 3)).to_np_array()
            array([1., 2., 0.], dtype=float32)
        """
        return array([self.x, self.y, self.z], dtype=float32)

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


if __name__ == "__main__":
    import doctest

    doctest.testmod()
