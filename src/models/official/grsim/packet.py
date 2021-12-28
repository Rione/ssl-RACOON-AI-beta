#!/usr/bin/env python3.10

"""packet.py

    This module contains:
        - SimPacket

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Packet.proto
"""


from models.official.grsim.replacement import Replacement
from models.official.grsim.commands import SimCommands


class SimPacket:
    """SimPacket

    Attributes:
        commands (SimCommands): Commands for the robots
        replacement (Replacement): Replacement for the robots
    """

    def __init__(self, commands: SimCommands, replacement: Replacement) -> None:

        self.commands: SimCommands = commands

        self.replacement: Replacement = replacement
