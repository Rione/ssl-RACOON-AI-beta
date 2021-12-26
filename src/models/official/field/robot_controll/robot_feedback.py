#!/usr/bin/env python3.10

"""robot_feedback.py

    This module is for the RobotFeedback class.
"""


from models.custom.robot_custom_feedback import RobotCustomFeedback


class RobotFeedback:
    """RobotFeedback

    Args:
        id (int): ID of the robot

    """

    def __init__(
        self, id: int, dribbler_ball_contact: bool, custom: RobotCustomFeedback
    ):

        self.__id: int = id

        self.__dribbler_ball_contact: bool = dribbler_ball_contact

        self.__custom: RobotCustomFeedback = custom

    def __str__(self):
        pass

    @property
    def id(self) -> int:
        """id

        Returns:
            int: ID of the robot
        """
        return self.__id

    @property
    def dribbler_ball_contact(self) -> bool:
        """dribbler_ball_contact

        Returns:
            bool: Dribbler ball contact of the robot
        """
        return self.__dribbler_ball_contact

    @property
    def custom(self) -> RobotCustomFeedback:
        """custom

        Returns:
            RobotCustomFeedback: Custom feedback of the robot
        """
        return self.__custom
