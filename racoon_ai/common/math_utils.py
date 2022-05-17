#!/usr/bin/env python3.10

"""math_utils.py

    This module contains
        - MathUtils
"""

from math import atan2, floor, pi, sqrt
from typing import Final

from racoon_ai.models.coordinate import Point, Pose


class MathUtils:
    """MathUtils

    This class contains
        - TWO_PI
        - PI_SQUARE
        - angle_normalize
        - angle_reduce
    """

    PI: Final[float] = pi

    TWO_PI: Final[float] = 2 * PI

    PI_SQUARE: Final[float] = pow(PI, 2)

    @staticmethod
    def distance(obj1: Point, obj2: Point) -> float:
        """distance

        Args:
            obj1 Point: object at least has x and y
            obj2 Point: object at least has x and y

        Returns:
            float: distance value
        """
        return sqrt(pow(obj1.x - obj2.x, 2) + pow(obj1.y - obj2.y, 2))

    @classmethod
    def radian(cls, obj1: Point, obj2: Point, center: float = 0) -> float:
        """radian

        Args:
            obj1 Point: object at least has x and y
            obj2 Point: object at least has x and y

        Returns:
            float: radian value

        Examples:
            >>> MathUtils.radian(Point(0, 0), Point(1, 1)) == MathUtils.PI / 4
            True
            >>> MathUtils.radian(Point(0, 0), Point(0, 1)) == MathUtils.PI / 2
            True
        """
        return cls.radian_normalize(atan2(obj2.y - obj1.y, obj2.x - obj1.x), center)

    @staticmethod
    def radian_normalize(angle: float, center: float = 0) -> float:
        """radian_normalize

        Normalize angle in `2 * pi` wide interval around center

        Args:
            angle (float): angle
            center (float, optional): center angle

        Returns:
            float: normalized angle

        Examples:
            Normalize in range `-pi` to `pi`:
                >>> MathUtils.radian_normalize(pi * 3 / 2) == - pi / 2
                True

            Normalize in range `0` to `2 * pi`:
                >>> MathUtils.radian_normalize((pi * 3 / 2), pi) == 3 * pi / 2
                True

        See Also:
            https://commons.apache.org/proper/commons-math/javadocs/api-3.1/org/apache/commons/math3/util/MathUtils.html#normalizeAngle(double,%20double)
        """
        return angle - (MathUtils.TWO_PI * floor((angle + MathUtils.PI - center) / MathUtils.TWO_PI))

    @staticmethod
    def radian_reduce(obj: (Pose | float), angle2: float, center: float = 0) -> float:
        """radian_reduce

        Args:
            obj (Pose | float): angle 1
            angle2 (float): angle 2
            center (float, optional): center angle value

        Returns:
            float: `angle1 - angle2` in `2 * pi` wide interval around center

        Examples:
            Difference in range `-pi` to `pi`:
                >>> pose = Pose(1, 2, (pi * 5 / 2))
                >>> MathUtils.radian_reduce(pose, pi) == - pi / 2
                True

                >>> MathUtils.radian_reduce(pose.theta, pi) == - pi / 2
                True

            Difference in range `0` to `2 * pi`:
                >>> pose = Pose(1, 2, (pi * 5 / 2))
                >>> MathUtils.radian_reduce(pose, pi, pi) == 3 * pi / 2
                True

                >>> MathUtils.radian_reduce(pose.theta, pi, pi) == 3 * pi / 2
                True
        """
        if isinstance(obj, Pose):
            return MathUtils.radian_normalize((obj.theta - angle2), center)
        return MathUtils.radian_normalize((obj - angle2), center)

    @staticmethod
    def __substitution_fn(pt1: Point, pt2: Point, pt3: Point) -> float:
        """substitution_fn

        The value of the line P1-P2, when point P3 is substituted.

        Args:
            pt1 (Point): point1
            pt2 (Point): point2
            pt3 (Point): point3

        Returns:
            float: The value at the pt3
        """
        return (pt2.x - pt1.x) * (pt3.y - pt1.y) - (pt2.y - pt1.y) * (pt3.x - pt1.x)

    @classmethod
    def has_intersection_with_line(cls, pt1: Point, pt2: Point, pt3: Point, pt4: Point) -> bool:
        """has_intersection_with_line

        Check if the line P1-P2 and P3-P4 intersect.

        Args:
            pt1 (Point): point1
            pt2 (Point): point2
            pt3 (Point): point3
            pt4 (Point): point4

        Returns:
            bool: whether the two lines intersect

        Examples:
            >>> MathUtils.has_intersection_with_line(Point(0, 0), Point(1, 1), Point(0, 1), Point(1, 0))
            True
        """
        val1 = cls.__substitution_fn(pt1, pt2, pt3)
        val2 = cls.__substitution_fn(pt1, pt2, pt4)
        val3 = cls.__substitution_fn(pt3, pt4, pt1)
        val4 = cls.__substitution_fn(pt3, pt4, pt2)
        return (val1 * val2 < 0) and (val3 * val4 < 0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
