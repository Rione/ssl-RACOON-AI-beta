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

        slipe_degree (float) : slope degree

        intercept (float) : ball intercept

        speed (float) : ball speed

        slope (float) : ball slope
    """

    def __init__(self) -> None:
        super().__init__(0, 0)
        self.__filtered_x: float = field(default=0, init=False)
        self.__filtered_y: float = field(default=0, init=False)
        self.__speed: float = field(default=0, init=False)
        self.__slope: float = field(default=0, init=False)
        self.__intercept: float = field(default=0, init=False)
        self.__slope_degree: float = field(default=0, init=False)

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
            f"slope_degree={self.slope_degree:.1f}, "
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
            f"slope_degree={self.slope_degree:.1f}, "
            ")"
        )

    @property
    def filtered_x(self) -> float:
        """confidence"""
        return self.__filtered_x

    @property
    def filtered_y(self) -> float:
        """confidence"""
        return self.__filtered_y

    @property
    def slope_degree(self) -> float:
        """confidence"""
        return self.__slope_degree

    @property
    def intercept(self) -> float:
        """confidence"""
        return self.__intercept

    @property
    def speed(self) -> float:
        """confidence"""
        return self.__speed

    @property
    def slope(self) -> float:
        """confidence"""
        return self.__slope

    def update(self, dball: Ball_Info) -> None:
        """update

        update this object with data from protobuf

        Args:
            ball (SSL_DetectionBall): ball proto message
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
        self.__slope_degree = dball.slope_degree
        self.__intercept = dball.intercept
        self.__speed = dball.speed
        self.__slope = dball.slope

    def to_pose(self) -> Pose:
        """to_pose

        convert this object to pose

        Returns:
            Pose: pose
        """
        return Pose(self.x, self.y, theta=0, z=self.z)
