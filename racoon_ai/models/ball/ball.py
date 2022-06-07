#!/usr/bin/env python3.10

"""ball.py
    This module contains:
        - Ball
"""

from racoon_ai.models.coordinate import Point
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Ball_Info


class Ball(Point):
    """Ball

    Attributes:
        x (float): x coordinate

        y (float): y coordinate

        z (float): z coordinate

        filtered (Point): filtered coordinate (x, y)

        filtered_x (float) : Kalman Filtered X

        filtered_y (float) : Kalman Filtered Y

        speed (float) : ball speed (absolute value)

        speed_slope (float) : ball slope

        speed_slope_radian (float) : speed slope angle in radian

        speed_intercept (float) : ball intercept
    """

    def __init__(self) -> None:
        super().__init__(0, 0)  # x, y, z
        self.__filtered: Point = Point(0, 0)
        self.__speed: float = float(0)
        self.__speed_slope: float = float(0)
        self.__speed_slope_radian: float = float(0)
        self.__speed_intercept: float = float(0)

    def __str__(self) -> str:
        return (
            "("
            f"pt=Point(x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f}), "
            f"filtered=Point(x={self.filtered_x:.1f}, y={self.filtered_y:.1f}), "
            f"speed={self.speed:.1f}, "
            f"speed_slope={self.speed_slope:.1f}, "
            f"speed_slope_radian={self.speed_slope_radian:.1f}, "
            f"speed_intercept={self.speed_intercept:.1f}"
            ")"
        )

    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def filtered(self) -> Point:
        """filtered

        get filtered point

        Returns:
            Point: filtered point

        Note:
            Z is not available in filtered point
        """
        return self.__filtered

    @property
    def filtered_x(self) -> float:
        """filtered_x"""
        return self.filtered.x

    @property
    def filtered_y(self) -> float:
        """filtered_y"""
        return self.filtered.y

    @property
    def speed(self) -> float:
        """speed

        speed of ball (absolute value)
        """
        return self.__speed

    @property
    def speed_slope(self) -> float:
        """slope

        slope of ball speed
        """
        return self.__speed_slope

    @property
    def speed_slope_radian(self) -> float:
        """speed_slope_radian

        slope of ball speed in radian
        """
        return self.__speed_slope_radian

    @property
    def speed_intercept(self) -> float:
        """speed_intercept

        intercept of ball speed with Y-axis
        """
        return self.__speed_intercept

    def update(self, dball: Ball_Info) -> None:
        """update

        update this object with data from protobuf

        Args:
            dball (Ball_Info): Ball_Info
        """
        self.__from_proto(dball)

    def __from_proto(self, dball: Ball_Info) -> None:
        """from_proto

        fill this object with data from protobuf

        Args:
            dball (SSL_DetectionBall): ball proto message
        """
        self.x = dball.x
        self.y = dball.y
        self.__filtered = Point(dball.filtered_x, dball.filtered_y)
        self.__speed = dball.speed
        self.__speed_slope = dball.slope
        self.__speed_slope_radian = dball.slope_radian
        self.__speed_intercept = dball.intercept

    def to_point(self) -> Point:
        """to_pose

        convert this object to pose

        Returns:
            Pose: pose
        """
        return Point(self.x, self.y, z=self.z)
