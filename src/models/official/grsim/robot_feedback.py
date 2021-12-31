#!/usr/bin/env python3.10

"""robot_feedback.py

    This module contains:
        - RobotFeedback
        - RobotControlFeedback

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/ssl_simulation_robot_feedback.proto
"""


from models.custom.robot_custom_feedback import RobotCustomFeedback
from models.official.grsim.error import SimError


class RobotFeedback:
    """RobotFeedback

    Args:
        id (int): ID of the robot
        dribbler_ball_contact (bool): Whether the robot is dribbling the ball
        custom (RobotCustomFeedback): Custom feedback for the robot
    """

    def __init__(
        self,
        id: int,
        dribbler_ball_contact: bool,
        custom: RobotCustomFeedback,
    ):

        self.__id: int = id

        self.__dribbler_ball_contact: bool = dribbler_ball_contact

        self.__custom: RobotCustomFeedback = custom

    def __str__(self) -> str:
        return (
            "RobotFeedback("
            f"id={self.id:2d} ,"
            f"dribbler_ball_contact={self.dribbler_ball_contact!s} ,"
            f"custom={self.custom!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "RobotFeedback("
            f"{self.id}, "
            f"{self.dribbler_ball_contact}, "
            f"{self.custom}"
            ")"
        )

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


class RobotControlResponse:
    """RobotControlResponse

    Args:
        errors (list[SimError]): List of errors, like using unsupported features
        feedback (list[RobotFeedback]): Feedback of the robot
    """

    def __init__(
        self,
        errors: list[SimError],
        feedback: list[RobotFeedback],
    ):

        self.__errors: list[SimError] = errors

        self.__feedback: list[RobotFeedback] = feedback

    def __str__(self) -> str:
        return (
            "RobotControlResponse("
            f"errors={self.errors!s}, "
            f"feedback={self.feedback!s}"
            ")"
        )

    def __repr__(self) -> str:
        return f"RobotControlResponse({self.errors}, {self.feedback})"

    @property
    def errors(self) -> list[SimError]:
        """errors

        Returns:
            list[SimError]: List of errors, like using unsupported features
        """
        return self.__errors

    @property
    def feedback(self) -> list[RobotFeedback]:
        """feedback

        Returns:
            list[RobotFeedback]: Feedback of the robot
        """
        return self.__feedback
