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
        id (int): ID of the robot
        kickspeedx (float): Kick speed in x direction
        kickspeedz (float): Kick speed in z direction
        veltangent (float): Velocity in the tangent direction
        velnormal (float): Velocity in the normal direction
        velangular (float): Velocity in the angular direction
        spinner (bool): Whether the dribller spins or not
        wheelsspeed (bool): Whether control by the each wheels or not
        wheel1 (float): Speed of the first wheel
        wheel2 (float): Speed of the second wheel
        wheel3 (float): Speed of the third wheel
        wheel4 (float): Speed of the fourth wheel
    """

    def __init__(
        self,
        id: int,
        kickspeedx: float,
        kickspeedz: float,
        veltangent: float,
        velnormal: float,
        velangular: float,
        spinner: bool,
        wheelsspeed: bool,
        wheel1: float,
        wheel2: float,
        wheel3: float,
        wheel4: float,
    ):

        self.id: int = id

        self.kickspeedx: float = kickspeedx

        self.kickspeedz: float = kickspeedz

        self.veltangent: float = veltangent

        self.velnormal: float = velnormal

        self.velangular: float = velangular

        self.spinner: bool = spinner

        self.wheelsspeed: bool = wheelsspeed

        self.wheel1: float = wheel1

        self.wheel2: float = wheel2

        self.wheel3: float = wheel3

        self.wheel4: float = wheel4

    def __str__(self) -> str:
        if not self.wheelsspeed:
            return (
                "RobotCommand("
                f"id={self.id} ,"
                f"kickspeedx={self.kickspeedx} ,"
                f"kickspeedz={self.kickspeedz} ,"
                f"veltangent={self.veltangent} ,"
                f"velnormal={self.velnormal} ,"
                f"velangular={self.velangular} ,"
                f"spinner={self.spinner} ,"
            )

        return (
            "RobotCommand("
            f"id={self.id:2d} ,"
            f"kickspeedx={self.kickspeedx:.1f} ,"
            f"kickspeedz={self.kickspeedz:.1f} ,"
            f"veltangent={self.veltangent:.2E} ,"
            f"velnormal={self.velnormal:.2E} ,"
            f"velangular={self.velangular:.2E} ,"
            f"spinner={self.spinner!s} ,"
            f"wheelsspeed={self.wheelsspeed!s} ,"
            f"wheel1={self.wheel1:.2E} ,"
            f"wheel2={self.wheel2:.2E} ,"
            f"wheel3={self.wheel3:.2E} ,"
            f"wheel4={self.wheel4:.2E} ,"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "RobotCommand("
            f"{self.id} ,"
            f"{self.kickspeedx} ,"
            f"{self.kickspeedz} ,"
            f"{self.veltangent} ,"
            f"{self.velnormal} ,"
            f"{self.velangular} ,"
            f"{self.spinner} ,"
            f"{self.wheelsspeed} ,"
            f"{self.wheel1} ,"
            f"{self.wheel2} ,"
            f"{self.wheel3} ,"
            f"{self.wheel4} ,"
            ")"
        )


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

        self.timestamp: float = timestamp

        self.isteamyellow: bool = isteamyellow

        self.robot_commands: list[RobotCommand] = robot_commands

    def __str__(self) -> str:
        return (
            "SimCommands("
            f"timestamp={self.timestamp:.2f} ,"
            f"isteamyellow={self.isteamyellow!s} ,"
            f"robot_commands={self.robot_commands!s} ,"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "SimCommands("
            f"{self.timestamp} ,"
            f"{self.isteamyellow} ,"
            f"{self.robot_commands} ,"
            ")"
        )
