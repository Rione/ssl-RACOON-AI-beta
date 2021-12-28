#!/usr/bin/env python3.10


"""common.py

    This module contains:
        - Team
        - RobotId
        - Division

    See also:
        https://github.com/RoboCup-SSL/ssl-game-controller/blob/master/proto/ssl_gc_common.proto
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


class RobotId:
    """RobotId

    Args:
        id (int): The id of the robot.
        team (Team): The team of the robot.
    """

    def __init__(self, id: int = -1, team: Team = Team.UNKNOWN) -> None:

        self.__id: int = id

        self.__team: Team = team

    def __str__(self) -> str:
        return f"RobotId(id={self.id}, team={self.team!s})"

    def __repr__(self) -> str:
        return f"RobotId({self.id}, {self.team})"

    @property
    def id(self) -> int:
        """id

        Returns:
            int: The id of the robot.
        """
        return self.__id

    @property
    def team(self) -> Team:
        """team

        Returns:
            Team: The team of the robot.
        """
        return self.__team


class Division(Enum):
    """Division

    This enum represents the possible divisions of the game.
    """

    DIV_UNKNOWN = 0

    DIV_A = 1

    DIV_B = 2
