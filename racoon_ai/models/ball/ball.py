#!/usr/bin/env python3.10

"""ball.py
    This module contains:
        - Ball
"""


from dataclasses import field

from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Ball_Info


class Ball(Point):
    """Ball

    Attributes:
        x (float): x coordinate

        y (float): y coordinate

        filtered_x (float) : Kalman Filtered X

        filtered_y (float) : Kalman Filtered Y

        slope_radian (float) : slope radian

        intercept (float) : ball intercept

        speed (float) : ball speed

        slope (float) : ball slope
    """

    def __init__(self) -> None:
        super().__init__(0, 0)
        self.__filtered_x: float = field(default=0, init=False)
        self.__filtered_y: float = field(default=0, init=False)
        self.__ball_speed: float = field(default=0, init=False)
        self.__ball_slope: float = field(default=0, init=False)
        self.__intercept: float = field(default=0, init=False)
        self.__slope_radian: float = field(default=0, init=False)

    def __str__(self) -> str:
        return (
            "Ball("
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"filtered_x={self.filtered_x:.1f}, "
            f"filtered_y={self.filtered_y:.1f}, "
            f"speed={self.speed:.1f}, "
            f"slope={self.slope:.1f}, "
            f"intercept={self.intercept:.1f}, "
            f"slope_degree={self.slope_radian:.1f}, "
            ")"
        )

    def __repr__(self) -> str:
        return (
            "Ball("
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"filtered_x={self.filtered_x:.1f}, "
            f"filtered_y={self.filtered_y:.1f}, "
            f"speed={self.speed:.1f}, "
            f"slope={self.slope:.1f}, "
            f"intercept={self.intercept:.1f}, "
            f"slope_degree={self.slope_radian:.1f}, "
            ")"
        )

    @property
    def filtered_x(self) -> float:
        """filtered_x"""
        return self.__filtered_x

    @property
    def filtered_y(self) -> float:
        """filtered_y"""
        return self.__filtered_y

    @property
    def slope_radian(self) -> float:
        """slope_radian"""
        return self.__slope_radian

    @property
    def intercept(self) -> float:
        """intercept"""
        return self.__intercept

    @property
    def speed(self) -> float:
        """speed

        speed of ball
        """
        return self.__ball_speed

    @property
    def slope(self) -> float:
        """slope

        slope of ball
        """
        return self.__ball_slope

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
        self.__slope_radian = dball.slope_radian
        self.__intercept = dball.intercept
        self.__ball_speed = dball.speed
        self.__ball_slope = dball.slope

    def to_pose(self) -> Pose:
        """to_pose

        convert this object to pose

        Returns:
            Pose: pose
        """
        return Pose(self.x, self.y, theta=0, z=self.z)
