#!/usr/bin/env python3.10

"""team.py

    This module contains the Team enum.
"""

from enum import Enum


class Team(Enum):
    """Team

    This enum represents the possible teams of the game.
    """

    # team not set
    UNKNOWN = 0

    YELLOW = 1

    BLUE = 2
