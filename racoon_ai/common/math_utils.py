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

    This class contains:
        - PI
        - TWO_PI
        - HALF_PI
        - PI_SQUARE
        - div_safe
        - distance
        - radian
        - radian_normalize
        - radian_reduce
        - has_intersection_with_line
    """

    PI: Final[float] = pi

    TWO_PI: Final[float] = 2 * PI

    HALF_PI: Final[float] = PI / 2

    PI_SQUARE: Final[float] = pow(PI, 2)

    @staticmethod
    def div_safe(val: float, designated: float = 1e-10) -> float:
        """div_safe
        judge if value is zero and return the designated

        Args:
            value (float): value to be judged
            designated (float): designated value if value is zero

        Returns:
            float: value
        """
        if val == 0:
            return designated
        return val

    @classmethod
    def distance(cls, obj1: Point, obj2: Point, safe: bool = True) -> float:
        """distance

        Args:
            obj1 Point: object at least has x and y
            obj2 Point: object at least has x and y
            safe (bool): if True, return non-zero value if value is zero

        Returns:
            float: distance value
        """
        if safe:
            return cls.div_safe(sqrt(pow(obj1.x - obj2.x, 2) + pow(obj1.y - obj2.y, 2)))
        return sqrt(pow(obj1.x - obj2.x, 2) + pow(obj1.y - obj2.y, 2))

    @classmethod
    def radian(cls, obj1: Point, obj2: Point, center: float = 0, safe: bool = True) -> float:
        """radian

        Args:
            obj1 (Point): object at least has x and y
            obj2 (Point): object at least has x and y
            center (float): center of radian
            safe (bool): if True, return non-zero result if result is zero

        Returns:
            float: radian value

        Examples:
            >>> MathUtils.radian(Point(0, 0), Point(1, 1)) == MathUtils.PI * (- 3 / 4)
            True
            >>> MathUtils.radian(Point(0, 0), Point(0, 1)) == MathUtils.PI * ( - 1/ 2)
            True
        """
        return cls.radian_normalize(atan2(obj1.y - obj2.y, obj1.x - obj2.x), center, safe)

    @classmethod
    def radian_normalize(cls, angle: float, center: float = 0, safe: bool = True) -> float:
        """radian_normalize

        Normalize angle in `2 * pi` wide interval around center

        Args:
            angle (float): angle
            center (float, optional): center angle
            safe (bool, optional): if True, return non-zero value if result is zero

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
        ret: float = angle - (cls.TWO_PI * floor((angle + cls.PI - center) / cls.TWO_PI))
        if safe:
            return cls.div_safe(ret)
        return ret

    @classmethod
    def radian_reduce(cls, obj1: (Pose | float), obj2: (Pose | float), center: float = 0) -> float:
        """radian_reduce

        Args:
            obj1 (Pose | float): angle 1
            obj2 (Pose | float): angle 2
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
        if isinstance(obj1, Pose):
            if isinstance(obj2, Pose):
                return cls.radian_normalize((obj1.theta - obj2.theta), center, False)
            return cls.radian_normalize((obj1.theta - obj2), center, False)

        if isinstance(obj2, Pose):
            return cls.radian_normalize((obj1 - obj2.theta), center, False)
        return cls.radian_normalize((obj1 - obj2), center, False)

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

    @classmethod
    def radian_neo(cls, obj1: Point, obj2: Point, center: float = 0) -> float:
        """radian
        Args:
            obj1 Point: object at least has x and y
            obj2 Point: object at least has x and y
        Returns:
            float: radian value
        """
        return cls.radian_normalize(atan2(obj1.y - obj2.y, obj1.x - obj2.x) - center)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
