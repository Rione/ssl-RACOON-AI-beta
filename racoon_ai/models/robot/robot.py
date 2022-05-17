#!/usr/bin/env python3.10

"""robot.py

    This module contains
        - Robot
"""

from dataclasses import field

from racoon_ai.models.coordinate import Pose
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Robot_Infos


class Robot(Pose):
    """
    Robot

    Args:
        robot_id (int): robot id

    Attributes:
        robot_id (int): robot id

        x (float): x coordinate

        y (float): y coordinate

        theta (float): orientation (radian) in the x-y plane

        distance_ball_robot (float): distance between ball and robot

        speed (float) : speed

        slope (float) : slope of velocity

        intercept (float) : intercept of velocity

        angular_velocity (float) : angular velocity

        is_ball_catch (bool) : is ball catched

        is_online (bool) : is robot online

        battery_voltage (float, optional) : battery voltage
    """

    def __init__(self, robot_id: int) -> None:
        super().__init__(0, 0)
        self.__robot_id: int = robot_id
        self.__distance_ball_robot: float = field(default=0, init=False)
        self.__degree_ball_robot: float = field(default=0, init=False)
        self.__speed: float = field(default=0, init=False)
        self.__slope: float = field(default=0, init=False)
        self.__intercept: float = field(default=0, init=False)
        self.__angular_velocity: float = field(default=0, init=False)
        self.__is_ball_catch: bool = field(default=False, init=False)
        self.__is_online: bool = field(default=False, init=False)
        self.__battery_voltage: float = field(default=0, init=False)

    def __str__(self) -> str:
        return (
            "Robot("
            f"robot_id={self.robot_id:2d}, "
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}, "
            f"distance_ball_robot={self.distance_ball_robot:.1f}, "
            f"speed={self.speed:.1f}, "
            f"slope={self.slope:.1f}, "
            f"intercept={self.intercept:.1f}, "
            f"angular_velocity={self.angular_velocity:.1f}, "
            f"ball_catch={self.is_ball_catch:1d}, "
            f"is_online={self.is_online:1d}, "
            f"battery_voltage={self.battery_voltage:.1f}, "
            ")"
        )

    def __repr__(self) -> str:
        return (
            "Robot("
            f"robot_id={self.robot_id:2d}, "
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}"
            ")"
        )

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Robot):
            return False
        return self.robot_id == obj.robot_id

    @property
    def distance_ball_robot(self) -> float:
        """distance_ball_robot"""
        return self.__distance_ball_robot

    @property
    def degree_ball_robot(self) -> float:
        """degree_ball_robot"""
        return self.__degree_ball_robot

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

    @property
    def is_ball_catch(self) -> bool:
        """is_ball_catch"""
        return self.__is_ball_catch

    @property
    def is_online(self) -> bool:
        """is_online"""
        return self.__is_online

    @property
    def battery_voltage(self) -> float:
        """battery_voltage"""
        return self.__battery_voltage

    def update(self, drobot: Robot_Infos) -> None:
        """
        Update robot

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
        """
        self.__from_proto(drobot)

    def __from_proto(self, dbot: Robot_Infos) -> None:
        """from_proto

        Args:
            drobot (SSL_DetectionRobot): SSL_DetectionRobot
            recv_time (int): receive time
        """
        self.x = dbot.x
        self.y = dbot.y
        self.theta = dbot.theta
        self.__distance_ball_robot = dbot.distance_ball_robot
        self.__degree_ball_robot = dbot.degree_ball_robot
        self.__speed = dbot.speed
        self.__slope = dbot.slope
        self.__intercept = dbot.intercept
        self.__angular_velocity = dbot.angular_velocity
        self.__is_ball_catch = dbot.ball_catch
        self.__is_online = dbot.online
        self.__battery_voltage = dbot.battery_voltage
