#!/usr/bin/env python3.10

"""robot.py

    This module contains
        - Robot
"""

from racoon_ai.models.coordinate import Point, Pose, Vector3f
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionRobot


class Robot(Pose):
    """
    Robot

    Args:
        robot_id (int): robot id

    Attributes:
        x (float): x coordinate

        y (float): y coordinate

        theta (float): orientation (radian) in the x-y plane

        z (float): z coordinate

        confidence (float): confidence

        robot_id (int): robot id

        pixel_point (Point): pixel point

        height (float): height

        velocity (Vector3f): velocity in the global coordinate system

        timestamp (float): timestamp
    """

    def __init__(self, robot_id: int) -> None:
        super().__init__(0, 0)
        self.__confidence: float = 0
        self.__robot_id: int = robot_id
        self.__pixel: Point = Point(0, 0)
        self.__height: float = 0
        self.__velocity: Vector3f = Vector3f(0, 0, 0)
        self.__timestamp: float = 0

    def __str__(self) -> str:
        return (
            "Robot("
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}, "
            f"z={self.z:.1f}, "
            f"confidence={self.confidence:3.0%}, "
            f"robot_id={self.robot_id:2d}, "
            f"pixel={self.pixel}, "
            f"height={self.height:.1f}, "
            f"velocity={self.velocity}, "
            ")"
        )

    def __repr__(self) -> str:
        return (
            "Robot("
            f"x={self.x}, "
            f"y={self.y}, "
            f"theta={self.theta}, "
            f"z={self.z}, "
            f"confidence={self.confidence}, "
            f"robot_id={self.robot_id}, "
            f"pixel={self.pixel}, "
            f"height={self.height}, "
            f"velocity={self.velocity}, "
            f"timestamp={self.timestamp}"
            ")"
        )

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Robot):
            return False
        return self.robot_id == obj.robot_id

    @property
    def confidence(self) -> float:
        """confidence"""
        return self.__confidence

    @property
    def robot_id(self) -> int:
        """robot id"""
        return self.__robot_id

    @property
    def pixel(self) -> Point:
        """pixel"""
        return self.__pixel

    @property
    def height(self) -> float:
        """height"""
        return self.__height

    @property
    def velocity(self) -> Vector3f:
        """velocity"""
        return self.__velocity

    @property
    def timestamp(self) -> float:
        """timestamp"""
        return self.__timestamp

    @classmethod
    def calc_velocity(cls, prev: "Robot", curr: "Robot", span: float) -> Vector3f:
        """
        calc_velocity

        Args:
            prev (Robot): previous robot
            curr (Robot): current robot
            span (float): time interval between previouse and current robot state

        Returns:
            Vector3f: velocity in (x, y, theta) format
        """
        if span < 1e-5:
            return Vector3f(0, 0, 0)

        # Calculate velocity
        delta_x = curr.x - prev.x
        delta_y = curr.y - prev.y
        delta_theta = curr.theta - prev.theta
        return Vector3f(delta_x / span, delta_y / span, delta_theta / span)

    def update(self, drobot: SSL_DetectionRobot, timestamp: float) -> None:
        """
        Update robot

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
        """
        span: float = timestamp - self.timestamp
        prev_robot: Robot = self
        self.__from_proto(drobot)
        self.__timestamp = timestamp
        self.__velocity = self.calc_velocity(self, prev_robot, span)

    def __from_proto(self, dbot: SSL_DetectionRobot) -> None:
        """from_proto

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
            recv_time (int): receive time
        """
        self.x = dbot.x
        self.y = dbot.y
        self.theta = dbot.orientation
        self.__confidence = dbot.confidence
        self.__pixel = Point(dbot.pixel_x, dbot.pixel_y)
        self.__height = dbot.height
