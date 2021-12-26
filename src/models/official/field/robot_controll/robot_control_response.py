#!/usr/bin/env python3.10

"""robot_controll_response.py

    This module is for the RobotControlResponse class.
"""


from models.official.field.robot_controll.robot_feedback import RobotFeedback


class RobotControlResponse:
    """RobotControlResponse

    Args:
        feedback (int): Feedback of the robot
    """

    def __init__(self, feedback: RobotFeedback):

        self.__feedback: RobotFeedback = feedback

    def __str__(self) -> str:
        pass

    @property
    def feedback(self) -> RobotFeedback:
        """feedback

        Returns:
            RobotFeedback: Feedback of the robot
        """
        return self.__feedback
