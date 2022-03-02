#!/usr/bin/env python3.10

"""intersection.py

    This module contains:
        - has_intersection

    See also:
        - https://github.com/kaityo256/find_intersection
"""

from racoon_ai.models.coordinate import Point


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


def has_intersection_with_line(pt1: Point, pt2: Point, pt3: Point, pt4: Point) -> bool:
    """has_intersection_with_line

    Check if the line P1-P2 and P3-P4 intersect.

    Args:
        pt1 (Point): point1
        pt2 (Point): point2
        pt3 (Point): point3
        pt4 (Point): point4

    Returns:
        bool: whether the two lines intersect
    """
    val1 = __substitution_fn(pt1, pt2, pt3)
    val2 = __substitution_fn(pt1, pt2, pt4)
    val3 = __substitution_fn(pt3, pt4, pt1)
    val4 = __substitution_fn(pt3, pt4, pt2)
    return (val1 * val2 < 0) and (val3 * val4 < 0)


def get_line_intersection(pt1: Point, pt2: Point, pt3: Point, pt4: Point) -> Point:
    """get_line_intersection

    Get the intersection point of two lines.

    Args:
        pt1 (Point): point1
        pt2 (Point): point2
        pt3 (Point): point3
        pt4 (Point): point4

    Returns:
        Point: intersection point
    """
    raise NotImplementedError
