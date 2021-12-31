#!/usr/bin/env python3.10

"""commands.py

    This module contains:
        - SimRobotCommand
        - SimCommands

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Commands.proto
"""


class RobotCommand:
    """RobotCommand

    Attributes:
        robot_id (int): ID of the robot
        kickpow (float, optional): Kick speed in horizontal direction
        kickpow_z (float, optinal): Kick speed in vertical direction
        vel_fwd (float, optional): Velocity in the forward direction
        vel_sway (float, optional): Velocity in the sideways direction
        vel_angular (float, optional): Velocity in the angular direction
        dribble_pow (float, optional): Dribbler power
        wheelsspeed (bool, optional): Whether control by the each wheels or not
        wheel1 (float, optional): Speed of the first wheel
        wheel2 (float, optional): Speed of the second wheel
        wheel3 (float, optional): Speed of the third wheel
        wheel4 (float, optional): Speed of the fourth wheel
        chip_enabled (bool, optional): Whether chip-kick is enabled or not
    """

    def __init__(
        self,
        robot_id: int,
        kickpow: float = 0,
        kickpow_z: float = 0,
        vel_fwd: float = 0,
        vel_sway: float = 0,
        vel_angular: float = 0,
        dribble_pow: float = 0,
        chip_enabled: bool = False,
        use_wheels_speed: bool = False,
        wheel1: float = 0,
        wheel2: float = 0,
        wheel3: float = 0,
        wheel4: float = 0,
    ):

        self.__robot_id: int = robot_id

        self.__kickpow: float = kickpow

        self.__kickpow_z: float

        if chip_enabled:
            self.__kickpow_z = kickpow_z
        else:
            self.__kickpow_z = 0

        self.__vel_fwd: float = vel_fwd

        self.__vel_sway: float = vel_sway

        self.__vel_angular: float = vel_angular

        self.__dribble_pow: float = dribble_pow

        self.__use_wheels_speed: bool = use_wheels_speed

        self.__wheel1: float = wheel1

        self.__wheel2: float = wheel2

        self.__wheel3: float = wheel3

        self.__wheel4: float = wheel4

        self.__chip_enabled: bool = chip_enabled

    def __str__(self) -> str:
        if not self.use_wheels_speed:
            if not self.chip_enabled:
                return (
                    "RobotCommand("
                    f"robot_id={self.robot_id:2d} ,"
                    f"vel_fwd={self.vel_fwd:.2E} ,"
                    f"vel_sway={self.vel_sway:.2E} ,"
                    f"vel_angular={self.vel_angular:.2E} ,"
                    f"kickpow={self.kickpow:.2f} ,"
                    f"dribble_pow={self.dribble_pow:.2E}"
                    ")"
                )

            return (
                "RobotCommand("
                f"robot_id={self.robot_id:2d} ,"
                f"vel_fwd={self.vel_fwd:.2E} ,"
                f"vel_sway={self.vel_sway:.2E} ,"
                f"vel_angular={self.vel_angular:.2E} ,"
                f"kickpow={self.kickpow:.2f} ,"
                f"kickpow_z={self.kickpow_z:.2E} ,"
                f"dribble_pow={self.dribble_pow:.2E}"
                ")"
            )

        if not self.chip_enabled:
            return (
                "RobotCommand("
                f"robot_id={self.robot_id:2d} ,"
                f"vel_fwd={self.vel_fwd:.2E} ,"
                f"vel_sway={self.vel_sway:.2E} ,"
                f"vel_angular={self.vel_angular:.2E} ,"
                f"kickpow={self.kickpow:.2f} ,"
                f"dribble_pow={self.dribble_pow:.2E} ,"
                f"wheel1={self.wheel1:.2E} ,"
                f"wheel2={self.wheel2:.2E} ,"
                f"wheel3={self.wheel3:.2E} ,"
                f"wheel4={self.wheel4:.2E}"
                ")"
            )

        return (
            "RobotCommand("
            f"robot_id={self.robot_id:2d} ,"
            f"vel_fwd={self.vel_fwd:.2E} ,"
            f"vel_sway={self.vel_sway:.2E} ,"
            f"vel_angular={self.vel_angular:.2E} ,"
            f"kickpow={self.kickpow:.2f} ,"
            f"kickpow_z={self.kickpow_z:.2E} ,"
            f"dribble_pow={self.dribble_pow:.2E} ,"
            f"wheel1={self.wheel1:.2E} ,"
            f"wheel2={self.wheel2:.2E} ,"
            f"wheel3={self.wheel3:.2E} ,"
            f"wheel4={self.wheel4:.2E}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "RobotCommand("
            f"robot_id={self.robot_id} ,"
            f"kickpow={self.kickpow} ,"
            f"kickpow_z={self.kickpow_z} ,"
            f"vel_fwd={self.vel_fwd} ,"
            f"vel_sway={self.vel_sway} ,"
            f"vel_angular={self.vel_angular} ,"
            f"dribble_pow{self.dribble_pow} ,"
            f"chip_enabled={self.chip_enabled}, "
            f"use_wheels_speed={self.use_wheels_speed} ,"
            f"wheel1={self.wheel1} ,"
            f"wheel2={self.wheel2} ,"
            f"wheel3={self.wheel3} ,"
            f"wheel4={self.wheel4}"
            ")"
        )

    @property
    def robot_id(self) -> int:
        """robot_id

        Returns:
            int: ID of the robot
        """
        return self.__robot_id

    @robot_id.setter
    def robot_id(self, value: int) -> None:
        """robot_id

        Args:
            value (int): ID of the robot
        """
        self.__robot_id = value

    @property
    def kickpow(self) -> float:
        """kickpow

        Returns:
            float: Kick speed in horizontal direction
        """
        return self.__kickpow

    @kickpow.setter
    def kickpow(self, value: float) -> None:
        """kickpow

        Args:
            value (float): Kick speed in horizontal direction
        """
        self.__kickpow = value

    @property
    def kickpow_z(self) -> float:
        """kickpow_z

        Returns:
            float: Kick speed in vertical direction
        """
        return self.__kickpow_z

    @kickpow_z.setter
    def kickpow_z(self, value: float) -> None:
        """kickpow_z

        Args:
            value (float): Kick speed in vertical direction
        """
        self.__kickpow_z = value

    @property
    def vel_fwd(self) -> float:
        """vel_fwd

        Returns:
            float: Velocity in the forward direction
        """
        return self.__vel_fwd

    @vel_fwd.setter
    def vel_fwd(self, value: float) -> None:
        """vel_fwd

        Args:
            value (float): Velocity in the forward direction
        """
        self.__vel_fwd = value

    @property
    def vel_sway(self) -> float:
        """vel_sway

        Returns:
            float: Velocity in the sideways direction
        """
        return self.__vel_sway

    @vel_sway.setter
    def vel_sway(self, value: float) -> None:
        """vel_sway

        Args:
            value (float): Velocity in the sideways direction
        """
        self.__vel_sway = value

    @property
    def vel_angular(self) -> float:
        """vel_angular

        Returns:
            float: Velocity in the angular direction
        """
        return self.__vel_angular

    @vel_angular.setter
    def vel_angular(self, value: float) -> None:
        """vel_angular

        Args:
            value (float): Velocity in the angular direction
        """
        self.__vel_angular = value

    @property
    def dribble_pow(self) -> float:
        """dribble_pow

        Returns:
            float: Dribble power
        """
        return self.__dribble_pow

    @dribble_pow.setter
    def dribble_pow(self, value: float) -> None:
        """dribble_pow

        Args:
            value (float): Dribble power
        """
        self.__dribble_pow = value

    @property
    def use_wheels_speed(self) -> bool:
        """use_wheels_speed

        Returns:
            bool: Use wheels speed
        """
        return self.__use_wheels_speed

    @use_wheels_speed.setter
    def use_wheels_speed(self, value: bool) -> None:
        """use_wheels_speed

        Args:
            value (bool): Use wheels speed
        """
        self.__use_wheels_speed = value

    @property
    def wheel1(self) -> float:
        """wheel1

        Returns:
            float: Wheel 1 speed
        """
        return self.__wheel1

    @wheel1.setter
    def wheel1(self, value: float) -> None:
        """wheel1

        Args:
            value (float): Wheel 1 speed
        """
        self.__wheel1 = value

    @property
    def wheel2(self) -> float:
        """wheel2

        Returns:
            float: Wheel 2 speed
        """
        return self.__wheel2

    @wheel2.setter
    def wheel2(self, value: float) -> None:
        """wheel2

        Args:
            value (float): Wheel 2 speed
        """
        self.__wheel2 = value

    @property
    def wheel3(self) -> float:
        """wheel3

        Returns:
            float: Wheel 3 speed
        """
        return self.__wheel3

    @wheel3.setter
    def wheel3(self, value: float) -> None:
        """wheel3

        Args:
            value (float): Wheel 3 speed
        """
        self.__wheel3 = value

    @property
    def wheel4(self) -> float:
        """wheel4

        Returns:
            float: Wheel 4 speed
        """
        return self.__wheel4

    @wheel4.setter
    def wheel4(self, value: float) -> None:
        """wheel4

        Args:
            value (float): Wheel 4 speed
        """
        self.__wheel4 = value

    @property
    def chip_enabled(self) -> bool:
        """chip_enabled

        Returns:
            bool: Chip enabled
        """
        return self.__chip_enabled

    @chip_enabled.setter
    def chip_enabled(self, value: bool) -> None:
        """chip_enabled

        Args:
            value (bool): Chip enabled
        """
        self.__chip_enabled = value


class SimCommands:
    """SimCommands

    Attributes:
        timestamp (float): Timestamp of the packet
        isteamyellow (bool): Whether the robot is on the yellow team
        robot_commands (list[SimRobotCommand]): Commands for the robots
    """

    def __init__(
        self,
        timestamp: float,
        isteamyellow: bool,
        robot_commands: list[RobotCommand],
    ) -> None:

        self.__timestamp: float = timestamp

        self.__isteamyellow: bool = isteamyellow

        self.__robot_commands: list[RobotCommand] = robot_commands

    def __str__(self) -> str:
        return (
            "SimCommands("
            f"timestamp={self.timestamp:.2f} ,"
            f"isteamyellow={self.isteamyellow!s} ,"
            f"robot_commands={self.robot_commands!s} ,"
            ")"
        )

    def __repr__(self) -> str:
        return "SimCommands(" f"{self.timestamp} ," f"{self.isteamyellow} ," f"{self.robot_commands} ," ")"

    @property
    def timestamp(self) -> float:
        """timestamp

        Returns:
            float: Timestamp of the packet
        """
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, value: float) -> None:
        """timestamp

        Args:
            value (float): Timestamp of the packet
        """
        self.__timestamp = value

    @property
    def isteamyellow(self) -> bool:
        """isteamyellow

        Returns:
            bool: Whether the robot is on the yellow team
        """
        return self.__isteamyellow

    @isteamyellow.setter
    def isteamyellow(self, value: bool) -> None:
        """isteamyellow

        Args:
            value (bool): Whether the robot is on the yellow team
        """
        self.__isteamyellow = value

    @property
    def robot_commands(self) -> list[RobotCommand]:
        """robot_commands

        Returns:
            list[RobotCommand]: Commands for the robots
        """
        return self.__robot_commands

    @robot_commands.setter
    def robot_commands(self, value: list[RobotCommand]) -> None:
        """robot_commands

        Args:
            value (list[RobotCommand]): Commands for the robots
        """
        self.__robot_commands = value
