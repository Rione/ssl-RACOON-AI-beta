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


@dataclass()
class RobotCommand:
    """RobotCommand

    Attributes:
        robot_id (int): ID of the robot
        chip_enabled (bool): Whether chip-kick is enabled or not
        use_wheels_speed (bool): Whether control by the each wheels or not
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

    vel_fwd: float = field(default=0, init=False)

    vel_sway: float = field(default=0, init=False)

    vel_angular: float = field(default=0, init=False)

    dribble_pow: float = field(default=0, init=False)

    kickpow: float = field(default=0, init=False)

    kickpow_z: float = field(default=0, init=False, kw_only=True)

    wheels: tuple[float, float, float, float] = field(default=(0, 0, 0, 0), init=False, kw_only=True)


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

    def append_robot_command(self, robot_command: RobotCommand) -> None:
        """append_robot_command

        Args:
            robot_command (RobotCommand): Robot command to add
        """
        self.robot_commands.append(robot_command)

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
