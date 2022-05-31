#!/usr/bin/env python3.10

"""robot.py

    This module contains
        - Robot
"""

from typing import Optional

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

        z (float): z coordinate

        distance_ball_robot (float): distance between ball and robot center

        radian_ball_robot (float): radian between ball and robot center

        speed (float) : speed (absolute value)

        speed_slope (float) : slope of speed

        speed_intercept (float) : intercept of speed

        vel_angular (float) : angular velocity (radian/s)

        is_ball_catched (bool) : is ball catched

        is_online (bool) : is robot online

        battery_voltage (float, optional) : battery voltage
    """

    def __init__(self, robot_id: int) -> None:
        super().__init__(0, 0)  # x, y, theta, z
        self.__robot_id: int = robot_id
        self.__distance_ball_robot: float = float(0)
        self.__radian_ball_robot: float = float(0)
        self.__speed: float = float(0)
        self.__speed_slope: float = float(0)
        self.__speed_intercept: float = float(0)
        self.__vel_angular: float = float(0)
        self.__is_ball_catched: bool = False
        self.__is_online: bool = False
        self.__battery_voltage: Optional[float] = None

    def __str__(self) -> str:
        if self.__battery_voltage is None:
            return (
                "("
                f"id={self.robot_id:2d}, "
                f"pose=Pose({self.x:.1f}, {self.y:.1f}, {self.theta:.1f}, {self.z:.1f}), "
                f"rad_ball_robot={self.radian_ball_robot:.1f}, "
                f"dist_ball_robot={self.distance_ball_robot:.1f}, "
                f"speed={self.speed:.1f}, "
                f"speed_slope={self.speed_slope:.1f}, "
                f"speed_intercept={self.speed_intercept:.1f}, "
                f"vel_angular={self.vel_angular:.1f}, "
                f"ball_catched={self.is_ball_catched:b}, "
                f"is_online={self.is_online:b}, "
                f"battery_vol={None}"
                ")"
            )

        return (
            "("
            f"id={self.robot_id:2d}, "
            f"pose=Pose({self.x:.1f}, {self.y:.1f}, {self.theta:.1f}, {self.z:.1f}), "
            f"radian_ball={self.radian_ball_robot:.1f}, "
            f"distance_ball={self.distance_ball_robot:.1f}, "
            f"speed={self.speed:.1f}, "
            f"speed_slope={self.speed_slope:.1f}, "
            f"speed_intercept={self.speed_intercept:.1f}, "
            f"vel_angular={self.vel_angular:.1f}, "
            f"ball_catched={self.is_ball_catched:b}, "
            f"is_online={self.is_online:b}, "
            f"battery_voltage={self.battery_voltage:3.1%}"
            ")"
        )

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Robot):
            return False
        return self.robot_id == obj.robot_id

    @property
    def distance_ball_robot(self) -> float:
        """distance_ball_robot"""
        return self.__distance_ball_robot

    @property
    def radian_ball_robot(self) -> float:
        """radian_ball_robot"""
        return self.__radian_ball_robot

    @property
    def robot_id(self) -> int:
        """robot id"""
        return self.__robot_id

    # pylint: disable=R0801
    @property
    def speed(self) -> float:
        """speed

        speed of robot (absolute value)
        """
        return self.__speed

    # pylint: disable=R0801
    @property
    def speed_slope(self) -> float:
        """speed_slope

        slope of robot speed
        """
        return self.__speed_slope

    # pylint: disable=R0801
    @property
    def speed_intercept(self) -> float:
        """speed_intercept

        intercept of robot speed relative t Y-axis
        """
        return self.__speed_intercept

    # pylint: disable=R0801
    @property
    def vel_angular(self) -> float:
        """vel_angular"""
        return self.__vel_angular

    @property
    def is_ball_catched(self) -> bool:
        """is_ball_catched"""
        return self.__is_ball_catched

    @property
    def is_online(self) -> bool:
        """is_online"""
        return self.__is_online

    @property
    def battery_voltage(self) -> Optional[float]:
        """battery_voltage"""
        return self.__battery_voltage

    def update(self, drobot: Robot_Infos) -> None:
        """
        Update robot

        Args:
            drobot (Robot_Infos): Robot_Infos
        """
        self.__from_proto(drobot)

    def __from_proto(self, dbot: Robot_Infos) -> None:
        """from_proto

        Args:
            drobot (Robot_Infos): Robot_Infos
        """
        self.x = dbot.x
        self.y = dbot.y
        self.theta = dbot.theta
        self.__distance_ball_robot = dbot.distance_ball_robot
        self.__radian_ball_robot = dbot.radian_ball_robot
        self.__speed = dbot.speed
        self.__speed_slope = dbot.slope
        self.__speed_intercept = dbot.intercept
        self.__vel_angular = dbot.angular_velocity
        self.__is_ball_catched = dbot.ball_catch
        self.__is_online = dbot.online
        self.__battery_voltage = dbot.battery_voltage

    def to_pose(self) -> Pose:
        """to_pose

        convert this object to pose

        Returns:
            Pose: pose of robot
        """
        return Pose(self.x, self.y, self.theta)


if __name__ == "__main__":
    bot1: Robot = Robot(1)
    print(f"bot1: {bot1}")
