#!/usr/bin/env python3.10

"""robot.py

    This module contains
        - Robot
"""

from typing import Optional

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Robot_Infos


class Robot(Pose):
    """
    Robot

    Args:
        robot_id (int): robot id

        is_imu_enabled (bool): is imu enabled

    Attributes:
        robot_id (int): robot id

        x (float): x coordinate

        y (float): y coordinate

        theta (float): orientation (radian) in the x-y plane

        z (float): z coordinate

        diff (Pose): difference between this and previous pose

        distance_ball_robot (float): distance between ball and robot center

        radian_ball_robot (float): radian between ball and robot center

        speed (float) : speed (absolute value)

        speed_slope (float) : slope of speed

        speed_intercept (float) : intercept of speed

        vel_angular (float) : angular velocity (radian/s)

        is_ball_catched (bool) : is ball catched

        is_online (bool) : is robot online

        is_visible (bool) : is robot visible

        battery_voltage (float, optional) : battery voltage
    """

    def __init__(self, robot_id: int, is_imu_enabled: bool = False) -> None:
        super().__init__(0, 0)  # x, y, theta, z
        self.__robot_id: int = robot_id
        self.__is_imu_enabled: bool = is_imu_enabled
        self.__diff: Pose = Pose(0, 0)
        self.__distance_ball_robot: float = float(0)
        self.__radian_ball_robot: float = float(0)
        self.__sec_par_frame: float = float(0)
        self.__speed: float = float(0)
        self.__speed_slope: float = float(0)
        self.__speed_intercept: float = float(0)
        self.__vel_angular: float = float(0)
        self.__is_ball_catched: bool = False
        self.__is_online: bool = False
        self.__is_visible: bool = False
        self.__battery_voltage: Optional[float] = None

    def __str__(self) -> str:
        msg: str = "("
        msg += f"id={self.robot_id:2d}, "
        msg += f"imu_enabled={self.is_imu_enabled!s}, "
        msg += f"pose=Pose{super().__str__()}, "
        msg += f"diff=Pose{self.diff!s}, "
        msg += f"vel=Pose{self.velocity!s} , "
        msg += f"rad_ball_robot={self.radian_ball_robot:.1f}, "
        msg += f"dist_ball_robot={self.distance_ball_robot:.1f}, "
        msg += f"speed={self.speed:.1f}, "
        msg += f"speed_slope={self.speed_slope:.1f}, "
        msg += f"speed_intercept={self.speed_intercept:.1f}, "
        msg += f"vel_angular={self.vel_angular:.1f}, "
        msg += f"ball_catched={self.is_ball_catched!s}, "
        msg += f"is_online={self.is_online!s}, "
        msg += f"is_visible={self.is_visible!s}, "
        msg += f"battery_vol={self.battery_voltage:.2E}" if self.battery_voltage is not None else "battery_vol=#N/A"
        msg += ")"
        return msg

    def __repr__(self) -> str:
        raise NotImplementedError

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Robot):
            return False
        return self.robot_id == obj.robot_id

    def __hash__(self) -> int:
        return hash(id(self))

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

    @property
    def is_imu_enabled(self) -> bool:
        """is_imu_enabled"""
        return self.__is_imu_enabled

    @property
    def diff(self) -> Pose:
        """diff

        diff between this and last pose

        NOTE: `diff.z` is not available now (always 0)
        """
        return self.__diff

    @property
    def velocity(self) -> Pose:
        """velocity

        velocity of robot

        Returns:
            Pose: velocity of robot
        """
        return Pose(
            self.diff.x / MU.div_safe(self.__sec_par_frame),
            self.diff.y / MU.div_safe(self.__sec_par_frame),
            self.diff.theta / MU.div_safe(self.__sec_par_frame),
            0,
        )

    @property
    def speed(self) -> float:  # pylint: disable=R0801
        """speed

        speed of robot (absolute value)

        Returns:
            float
        """
        return self.__speed

    @property
    def speed_slope(self) -> float:  # pylint: disable=R0801
        """speed_slope

        slope of robot speed

        Returns:
            float
        """
        return self.__speed_slope

    @property
    def speed_intercept(self) -> float:  # pylint: disable=R0801
        """speed_intercept

        intercept of robot speed relative t Y-axis

        Returns:
            float
        """
        return self.__speed_intercept

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
    def is_visible(self) -> bool:
        """is_visible"""
        return self.__is_visible

    @property
    def battery_voltage(self) -> Optional[float]:
        """battery_voltage"""
        return self.__battery_voltage

    def update(self, drobot: Robot_Infos, sec_par_frame: float) -> None:
        """
        Update robot

        Args:
            drobot (Robot_Infos): Robot_Infos
        """
        self.__from_proto(drobot)
        self.__sec_par_frame = sec_par_frame

    def __from_proto(self, dbot: Robot_Infos) -> None:
        """from_proto

        Args:
            drobot (Robot_Infos): Robot_Infos
        """
        self.x = dbot.x
        self.y = dbot.y
        self.theta = dbot.theta
        self.__diff = Pose(dbot.diff_x, dbot.diff_y, dbot.diff_theta, 0)
        self.__distance_ball_robot = dbot.distance_ball_robot
        self.__radian_ball_robot = dbot.radian_ball_robot
        self.__speed = dbot.speed
        self.__speed_slope = dbot.slope
        self.__speed_intercept = dbot.intercept
        self.__vel_angular = dbot.angular_velocity
        self.__is_ball_catched = dbot.ball_catch
        self.__is_online = dbot.online
        self.__is_visible = dbot.visible
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
