#!/usr/bin/env python3.10

"""robot_id.py

    This module contains the RobotId class.
"""

from models.official.game_controller.team import Team


class RobotId:
    """RobotId

    Args:
        id (int): The id of the robot.
        team (Team): The team of the robot.
    """

    def __init__(self, id: int, team: Team):

        self.__id: int = id

        self.__team: Team = team

    def __str__(self):
        pass
