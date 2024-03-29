#!/usr/bin/env python3.10

"""geometry.py

    This module contains
        - Geometry
"""

from racoon_ai.models.coordinate import Point
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Geometry_Info


class Geometry:
    """
    Geometry

    Attributes:
        field_length (int): length of field

        field_width (int): width of field

        goal_width (int): width of goal

        goal_width_half (float): width of goal / 2

        goal_depth (int): depth of goal

        boundary_width (int): width of boundary

        penalty_area_depth (int): depth of penalty

        penalty_area_width (int): width of penalty

        penalty_area_width_half (float): width of penalty / 2

        center_circle_radius (int): radius of center circle

        line_thickness (int): thickness of line

        goal_center_to_penalty_mark (int): distance between goal center to penalty

        goal_height (int) : height of goal

        ball_radius (float): radius of ball

        max_robot_radius (float): max robot radius

        goal (Point): goal (x, y)

        goal_x (float): goal x

        goal_y (float): goal y
    """

    def __init__(self) -> None:
        self.__field_length: int = int(0)
        self.__field_width: int = int(0)
        self.__goal_width: int = int(0)
        self.__goal_depth: int = int(0)
        self.__boundary_width: int = int(0)
        self.__penalty_area_depth: int = int(0)
        self.__penalty_area_width: int = int(0)
        self.__center_circle_radius: int = int(0)
        self.__line_thickness: int = int(0)
        self.__goal_center_to_penalty_mark: int = int(0)
        self.__goal_height: int = int(0)
        self.__ball_radius: float = float(0)
        self.__max_robot_radius: float = float(0)
        self.__goal: Point = Point(0, 0)

    def __str__(self) -> str:
        return (
            "("
            f"field_length={self.field_length:1d}, "
            f"field_width={self.field_width:1d}, "
            f"goal_width={self.goal_width:1d}, "
            f"goal_width_half={self.goal_width_half:f}, "
            f"goal_depth={self.goal_depth:1d}, "
            f"boundary_width={self.boundary_width:1d}, "
            f"penalty_area_width={self.penalty_area_width:1d}, "
            f"penalty_area_width_half={self.penalty_area_width_half:f}, "
            f"penalty_area_depth={self.penalty_area_depth:1d}, "
            f"center_circle_radius={self.center_circle_radius:1d}, "
            f"line_thickness={self.line_thickness:1d}, "
            f"goal_center_to_penalty_mark={self.goal_center_to_penalty_mark:1d}, "
            f"goal_height={self.goal_height:1d}, "
            f"ball_radius={self.ball_radius:.1f}, "
            f"max_robot_radius={self.max_robot_radius:.1f}, "
            f"goal=Point(x={self.goal.x:.1f}, y={self.goal.y:.1f})"
            ")"
        )

    @property
    def field_length(self) -> int:
        """field_length"""
        return self.__field_length

    @property
    def field_width(self) -> int:
        """field_width"""
        return self.__field_width

    @property
    def goal_width(self) -> int:
        """goal_width"""
        return self.__goal_width

    @property
    def goal_width_half(self) -> float:
        """goal_width"""
        return self.__goal_width / 2

    @property
    def goal_depth(self) -> int:
        """goal_depth"""
        return self.__goal_depth

    @property
    def boundary_width(self) -> int:
        """boundary_width"""
        return self.__boundary_width

    @property
    def penalty_area_depth(self) -> int:
        """penalty_area_depth"""
        return self.__penalty_area_depth

    @property
    def penalty_area_width(self) -> int:
        """penalty_area_width"""
        return self.__penalty_area_width

    @property
    def penalty_area_width_half(self) -> float:
        """penalty_area_width"""
        return self.__penalty_area_width / 2

    @property
    def center_circle_radius(self) -> int:
        """center_circle_radius"""
        return self.__center_circle_radius

    @property
    def line_thickness(self) -> int:
        """line_thickness"""
        return self.__line_thickness

    @property
    def goal_center_to_penalty_mark(self) -> int:
        """goal_center_to_penalty_mark"""
        return self.__goal_center_to_penalty_mark

    @property
    def goal_height(self) -> int:
        """goal_height"""
        return self.__goal_height

    @property
    def ball_radius(self) -> float:
        """ball_radius"""
        return self.__ball_radius

    @property
    def max_robot_radius(self) -> float:
        """max_robot_radius"""
        return self.__max_robot_radius

    @property
    def goal(self) -> Point:
        """goal"""
        return self.__goal

    @property
    def their_goal(self) -> Point:
        """their_goal"""
        return Point(-self.goal.x, -self.goal.y)

    def update(self, geometry: Geometry_Info, attack_direction: int) -> None:
        """
        Update robot

        Args:
            geometry (Geometry_Info): Geometry_Info
            attack_direction (int): attack direction
        """
        self.__from_proto(geometry, attack_direction)

    def __from_proto(self, geometry: Geometry_Info, atttack_direction: int) -> None:
        """from_proto

        Args:
            geometry (Geometry_Info): Geometry_Info
            attack_direction (int): attack direction
        """
        self.__field_length = geometry.field_length
        self.__field_width = geometry.field_width
        self.__goal_width = geometry.goal_width
        self.__goal_depth = geometry.goal_depth
        self.__boundary_width = geometry.boundary_width
        self.__penalty_area_width = geometry.penalty_area_width
        self.__penalty_area_depth = geometry.penalty_area_depth
        self.__center_circle_radius = geometry.center_circle_radius
        self.__line_thickness = geometry.line_thickness
        self.__goal_center_to_penalty_mark = geometry.goal_center_to_penalty_mark
        self.__goal_height = geometry.goal_height
        self.__ball_radius = geometry.ball_radius
        self.__max_robot_radius = geometry.max_robot_radius
        self.__goal = Point(geometry.goal_x, geometry.goal_y)

        # Override (vision problem)
        if atttack_direction < 0:
            self.__goal = Point(4500, 0)
        else:
            self.__goal = Point(-4500, 0)
        self.__goal_width = int(1200)
        self.__center_circle_radius = int(500)
        self.__penalty_area_width = int(2400)
        self.__penalty_area_depth = int(1200)
