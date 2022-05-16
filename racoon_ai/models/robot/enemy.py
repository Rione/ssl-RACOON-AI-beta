#!/usr/bin/env python3.10

"""enemy.py

    This module contains
        - Enemy
"""

from dataclasses import field

from racoon_ai.models.coordinate import Pose
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Enemy_Infos


class Enemy(Pose):
    """
    Enemy

    Args:
        robot_id (int): robot id

    Attributes:
        robot_id (int): robot id

        x (float): x coordinate

        y (float): y coordinate

        theta (float): orientation (radian) in the x-y plane

        speed (float) : speed

        slope (float) : slope of velocity

        intercept (float) : intercept of velocity

        angular_velocity (float) : angular velocity

    """

    def __init__(self, robot_id: int) -> None:
        super().__init__(0, 0)
        self.__robot_id: int = robot_id
        self.__speed: float = field(default=0, init=False)
        self.__slope: float = field(default=0, init=False)
        self.__intercept: float = field(default=0, init=False)
        self.__angular_velocity: float = field(default=0, init=False)

    def __str__(self) -> str:
        return (
            "Robot("
            f"robot_id={self.robot_id:2d}, "
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}, "
            f"speed={self.speed:.1f}, "
            f"slope={self.slope:.1f}, "
            f"intercept={self.intercept:.1f}, "
            f"angular_velocity={self.angular_velocity:.1f}, "
            ")"
        )

    def __repr__(self) -> str:
        return (
            "Robot("
            f"robot_id={self.robot_id:2d}, "
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}, "
            f"speed={self.speed:.1f}, "
            f"slope={self.slope:.1f}, "
            f"intercept={self.intercept:.1f}, "
            f"angular_velocity={self.angular_velocity:.1f}, "
            ")"
        )

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Enemy):
            return False
        return self.robot_id == obj.robot_id

    @property
    def robot_id(self) -> int:
        """robot id"""
        return self.__robot_id

    @property
    def speed(self) -> float:
        """speed"""
        return self.__speed

    @property
    def slope(self) -> float:
        """slope"""
        return self.__slope

    @property
    def intercept(self) -> float:
        """intercept"""
        return self.__intercept

    @property
    def angular_velocity(self) -> float:
        """angular_velocity"""
        return self.__angular_velocity

    def update(self, drobot: Enemy_Infos) -> None:
        """
        Update robot

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
        """
        self.__from_proto(drobot)

    def __from_proto(self, dbot: Enemy_Infos) -> None:
        """from_proto

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
            recv_time (int): receive time
        """
        self.x = dbot.x
        self.y = dbot.y
        self.theta = dbot.theta
        self.__speed = dbot.speed
        self.__slope = dbot.slope
        self.__intercept = dbot.intercept
        self.__angular_velocity = dbot.angular_velocity
