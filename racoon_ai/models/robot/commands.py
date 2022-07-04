#!/usr/bin/env python3.10

"""commands.py

    This module contains:
        - RobotCommand
        - SimCommands

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Commands.proto
"""

from dataclasses import dataclass, field
from time import time
from typing import Optional

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Robot_Command


@dataclass()
class RobotCommand:
    """RobotCommand

    Attributes:
        robot_id (int): ID of the robot
        chip_enabled (bool): Whether chip-kick is enabled or not
        use_wheels_speed (bool): Whether control by the each wheels or not
        use_imu (bool): Whether control by the IMU or not
        vel_fwd (float): Velocity in the forward direction
        vel_sway (float): Velocity in the sideways direction
        vel_angular (float): Velocity in the angular direction
        dribble_pow (float): Dribbler power
        kickpow (float): Kick speed in horizontal direction
        kickpow_z (float): Kick speed in vertical direction
        wheels (tuple[float, float, float, float]): Speed of the first wheel
    """

    robot_id: int = field()

    chip_enabled: bool = field(default=False, kw_only=True)

    use_wheels_speed: bool = field(default=False, kw_only=True)

    use_imu: bool = field(default=False, kw_only=True)

    vel_fwd: float = field(default_factory=float, init=False)

    vel_sway: float = field(default_factory=float, init=False)

    vel_angular: float = field(default_factory=float, init=False)

    dribble_pow: float = field(default_factory=float, init=False)

    kickpow: float = field(default_factory=float, init=False)

    kickpow_z: float = field(default_factory=float, init=False)

    wheels: tuple[float, float, float, float] = field(default=(float(0), float(0), float(0), float(0)), init=False)

    target_pose: Pose = field(default=Pose(0, 0), init=False)

    def __str__(self) -> str:
        msg: str = "("
        msg += f"id={self.robot_id:02d} "
        msg += "(chip_eabled), " if self.chip_enabled else ""
        msg += "(imu_enabled), " if self.use_imu else ""
        msg += f"vel_fwd={self.vel_fwd:.2E}, " if not self.use_wheels_speed else ""
        msg += f"vel_sway={self.vel_sway:.2E}, " if not self.use_wheels_speed else ""
        msg += f"vel_angular={self.vel_angular:.2E}, " if not (self.use_wheels_speed or self.use_imu) else ""
        msg += f"target_pose={self.target_pose!s}, " if self.use_imu else ""
        msg += f"dribble_pow={self.dribble_pow:.2E}, "
        msg += f"kickpow={self.kickpow:.2E}, "
        msg += f"kickpow_z={self.kickpow_z:.2E}, " if self.chip_enabled else ""
        msg += f"wheels={self.wheels}" if self.use_wheels_speed else ""
        msg += ")"
        return msg

    def to_proto(self) -> grSim_Robot_Command:
        """to_proto

        Returns:
            grSim_Robot_Command: grSim_Robot_Command
        """
        proto = grSim_Robot_Command()

        # Required
        proto.id = self.robot_id
        proto.kickspeedx = self.kickpow
        proto.kickspeedz = self.kickpow_z if self.chip_enabled else float(0)
        proto.veltangent = self.vel_fwd
        proto.velnormal = self.vel_sway
        proto.velangular = self.vel_angular if (not self.use_imu) else MU.radian_normalize(self.target_pose.theta)
        proto.spinner = bool(self.dribble_pow)
        proto.wheelsspeed = self.use_wheels_speed

        # Optional
        if self.use_wheels_speed:
            proto.wheel1 = self.wheels[0]
            proto.wheel2 = self.wheels[1]
            proto.wheel3 = self.wheels[2]
            proto.wheel4 = self.wheels[3]

        return proto


@dataclass()
class RobotCustomCommand:
    """RobotCustomCommand

    A custom command for our robots.

    Attributes:
        is_emergency_pressed (bool): True if the emergency button is pressed.
    """

    is_emergency_pressed: bool = field(default=False)


@dataclass()
class SimCommands:
    """SimCommands

    Attributes:
        timestamp (float): Timestamp of the packet
        isteamyellow (bool): Whether the robot is on the yellow team
        robot_commands (list[SimRobotCommand]): Commands for the robots
    """

    timestamp: float = field(default=time(), init=False)

    isteamyellow: bool = field(default=False)

    robot_commands: list[RobotCommand] = field(default_factory=list[RobotCommand])

    def get_robot_command(self, robot_id: int) -> Optional[RobotCommand]:
        """get_robot_command

        Args:
            robot_id (int): ID of the robot

        Returns:
            Optional[RobotCommand]: Robot command
        """
        for robot_command in self.robot_commands:
            if robot_command.robot_id == robot_id:
                return robot_command
        return None

    def to_proto(self) -> list[grSim_Robot_Command]:
        """to_proto

        Returns:
            list[grSim_Robot_Command]: grSim_Robot_Command
        """
        return [robot_command.to_proto() for robot_command in self.robot_commands]
