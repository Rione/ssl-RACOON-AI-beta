#!/usr/bin/env python3.10

"""command.py

    This module contains the Command enum.
"""

from enum import Enum


class Command(Enum):
    """Command

    This enum represents the possible commands that can be sent by the game controller.
    """

    HALT = 0

    STOP = 1

    NORMAL_START = 2

    FORCE_START = 3

    PREPARE_KICKOFF_YELLOW = 4

    PREPARE_KICKOFF_BLUE = 5

    PREPARE_PENALTY_YELLOW = 6

    PREPARE_PENALTY_BLUE = 7

    DIRECT_FREE_YELLOW = 8

    DIRECT_FREE_BLUE = 9

    INDIRECT_FREE_YELLOW = 10

    INDIRECT_FREE_BLUE = 11

    TIMEOUT_YELLOW = 12

    TIMEOUT_BLUE = 13

    # DEPRECATED
    GOAL_YELLOW = 14

    # DEPRICATED
    GOAL_BLUE = 15

    BALL_PLACEMENT_YELLOW = 16

    BALL_PLACEMENT_BLUE = 17
