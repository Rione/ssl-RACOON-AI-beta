#!/usr/bin/env python3.10

"""packet.py

    This module contains:
        - SimPacket

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Packet.proto
"""


from models.official.grsim.commands import SimCommands
from models.official.grsim.replacement import Replacement


class SimPacket:
    """SimPacket

    Attributes:
        commands (SimCommands): Commands for the robots
        replacement (Replacement): Replacement commands
    """

    def __init__(self, commands: SimCommands, replacement: Replacement) -> None:

        self.__commands: SimCommands = commands

        self.__replacement: Replacement = replacement

    def __str__(self) -> str:
        return (
            "SimPacket("
            f"commands={self.commands!s}, "
            f"replacement={self.replacement!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "SimPacket("
            f"commands={self.commands}, "
            f"replacement={self.replacement}"
            ")"
        )

    @property
    def commands(self) -> SimCommands:
        """commands

        Returns:
            SimCommands: Commands for the robots
        """
        return self.__commands

    @commands.setter
    def commands(self, value: SimCommands) -> None:
        """commands

        Args:
            value (SimCommands): Commands for the robots
        """
        self.__commands = value

    @property
    def replacement(self) -> Replacement:
        """replacement

        Returns:
            Replacement: Replacement commands
        """
        return self.__replacement

    @replacement.setter
    def replacement(self, value: Replacement) -> None:
        """replacement

        Args:
            value (Replacement): Replacement commands
        """
        self.__replacement = value
