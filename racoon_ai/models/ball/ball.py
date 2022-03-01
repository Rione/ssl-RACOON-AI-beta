#!/usr/bin/env python3.10

"""ball.py
    This module contains:
        - Ball
"""

from racoon_ai.models.coordinate import Point, Vector3f
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall


class Ball(Point):
    """Ball

    Attributes:
        x (float): x coordinate

        y (float): y coordinate

        z (float): z coordinate

        confidence (float): confidence

        area (float): area

        pixel_point (Point): pixel point

        velocity (Vector3f): velocity

        timestamp (float): timestamp
    """

    def __init__(self) -> None:
        super().__init__(0, 0)
        self.__confidence: float = 0
        self.__area: float = 0
        self.__pixel: Point = Point(0, 0)
        self.__velocity: Vector3f = Vector3f(0, 0, 0)
        self.__timestamp: float = 0

    def __str__(self) -> str:
        return (
            "Ball("
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"z={self.z:.1f}, "
            f"confidence={self.confidence:3.0%}, "
            f"area={self.area:.1f}, "
            f"pixel={self.pixel}, "
            f"velocity={self.velocity}, "
            ")"
        )

    def __repr__(self) -> str:
        return (
            "Ball("
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"confidence={self.confidence}, "
            f"area={self.area}, "
            f"pixel={self.pixel}, "
            f"velocity={self.velocity}, "
            f"timestamp={self.timestamp}"
            ")"
        )

    @property
    def confidence(self) -> float:
        """confidence"""
        return self.__confidence

    @property
    def area(self) -> float:
        """area"""
        return self.__area

    @property
    def pixel(self) -> Point:
        """pixel"""
        return self.__pixel

    @property
    def velocity(self) -> Vector3f:
        """velocity"""
        return self.__velocity

    @property
    def timestamp(self) -> float:
        """timestamp"""
        return self.__timestamp

    @classmethod
    def calc_velocity(cls, curr_ball: "Ball", prev_ball: "Ball", span: float) -> Vector3f:
        """calc_velocity

        calculate velocity

        Args:
            curr_ball (Ball): current ball state
            prev_ball (Ball): previous ball state
            span (int): time interval between current and previous ball state

        Returns:
            Vector3f: velocity in (x, y, z) format
        """
        # Greater than 60[Hz] exeption
        if span < 16e-3:
            return Vector3f(0, 0, 0)

        # Calculate velocity
        delta = curr_ball - prev_ball
        return Vector3f((delta.x ** 2) / span, (delta.y ** 2) / span, (delta.z ** 2) / span)

    def update(self, dball: SSL_DetectionBall, timestamp: float) -> None:
        """update

        update this object with data from protobuf

        Args:
            ball (SSL_DetectionBall): ball proto message
        """
        prev_ball: Ball = self
        self.__from_proto(dball)
        self.__timestamp = timestamp
        span: float = self.timestamp - prev_ball.timestamp
        vel: Vector3f = self.calc_velocity(self, prev_ball, span)
        self.__velocity = vel

    def __from_proto(self, dball: SSL_DetectionBall) -> None:
        """from_proto

        fill this object with data from protobuf

        Args:
            dball (SSL_DetectionBall): ball proto message
        """
        self.x = dball.x
        self.y = dball.y
        self.z = dball.z
        self.__confidence = dball.confidence
        self.__area = dball.area
        self.__pixel = Point(dball.pixel_x, dball.pixel_y)
