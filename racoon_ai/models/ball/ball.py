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

        filtered_x (float) : Kalman Filtered X

        filtered_y (float) : Kalman Filtered Y

        speed (float) : ball speed (absolute value)

        speed_slope (float) : ball slope

        speed_slope_radian (float) : speed slope angle in radian

        speed_intercept (float) : ball intercept
    """

    def __init__(self) -> None:
        super().__init__(0, 0)  # x, y, z
        self.__filtered_x: float = float(0)
        self.__filtered_y: float = float(0)
        self.__speed: float = float(0)
        self.__speed_slope: float = float(0)
        self.__speed_slope_radian: float = float(0)
        self.__speed_intercept: float = float(0)

    def __str__(self) -> str:
        return (
            "("
            f"pt=Point(x={self.x:.1f}, y={self.y:.1f}, z={self.z:.1f}), "
            f"filtered_x={self.filtered_x:.1f}, "
            f"filtered_y={self.filtered_y:.1f}, "
            f"speed={self.speed:.1f}, "
            f"speed_slope={self.speed_slope:.1f}, "
            f"speed_slope_radian={self.speed_slope_radian:.1f}, "
            f"speed_intercept={self.speed_intercept:.1f}, "
            ")"
        )

    def __repr__(self) -> str:
        raise NotImplementedError

    @property
    def filtered_x(self) -> float:
        """filtered_x"""
        return self.__filtered_x

    @property
    def filtered_y(self) -> float:
        """filtered_y"""
        return self.__filtered_y

    # pylint: disable=R0801
    @property
    def speed(self) -> float:
        """speed

        speed of ball
        """
        return self.__speed

    # pylint: disable=R0801
    @property
    def speed_slope(self) -> float:
        """slope

        slope of ball speed
        """
        return self.__speed_slope

    # pylint: disable=R0801
    @property
    def speed_slope_radian(self) -> float:
        """speed_slope_radian"""
        return self.__speed_slope_radian

    # pylint: disable=R0801
    @property
    def speed_intercept(self) -> float:
        """speed_intercept"""
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
        self.__filtered_x = dball.filtered_x
        self.__filtered_y = dball.filtered_y
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
