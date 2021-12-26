#!/usr/bin/env python3.10

"""detection_frame.py

   This module contains the DetectionFrame class.
   DetectionFrame is a class that contains the detection results for a single frame.
"""

from models.official.field.detection.detection_ball import DetectionBall
from models.official.field.detection.detection_robot import DetectionRobot


class DetectionFrame:
    """DetectionFrame

    Args:
        frame_number (int): The frame number.
        t_capture (float): The time at which the frame was captured.
        t_sent (float): The time at which the frame was sent.
        camera_id (int): The camera id.
        balls (list[DetectionBall]): The list of detected balls.
        robots_yellow (list[DetectionRobot]): The list of yellow detected robots.
        robots_blue (list[DetectionRobot]): The list of blue detected robots.
    """

    def __init__(
        self,
        frame_number: int,
        t_capture: float,
        t_sent: float,
        camera_id: int,
        balls: list[DetectionBall],
        robots_yellow: list[DetectionRobot],
        robots_blue: list[DetectionRobot],
    ):

        self.__frame_number: int = frame_number

        self.__t_capture: float = t_capture

        self.__t_sent: float = t_sent

        self.__camera_id: int = camera_id

        self.__balls: list[DetectionBall] = balls

        self.__robots_yellow: list[DetectionRobot] = robots_yellow

        self.__robots_blue: list[DetectionRobot] = robots_blue

    def __str__(self):
        # TODO: balls, robots_yellow, robots_blue
        return "DetectionFrame(%d, %.2f, %.2f, %d, %s, %s, %s)" % (
            self.__frame_number,
            self.__t_capture,
            self.__t_sent,
            self.__camera_id,
            "Undefined",
            "Undefined",
            "Undefined",
        )

    @property
    def frame_number(self) -> int:
        """frame_number

        Returns:
            int: The frame number.
        """
        return self.__frame_number

    @property
    def t_capture(self) -> float:
        """t_capture

        Returns:
            float: The time at which the frame was captured.
        """
        return self.__t_capture

    @property
    def t_sent(self) -> float:
        """t_sent

        Returns:
            float: The time at which the frame was sent.
        """
        return self.__t_sent

    @property
    def camera_id(self) -> int:
        """camera_id

        Returns:
            int: The id of camera.
        """
        return self.__camera_id

    @property
    def balls(self) -> list[DetectionBall]:
        """balls

        Returns:
            list[DetectionBall]: The list of detected balls.
        """
        return self.__balls

    @property
    def robots_yellow(self) -> list[DetectionRobot]:
        """robots_yellow

        Returns:
            list[DetectionRobot]: The list of yellow detected robots.
        """
        return self.__robots_yellow

    @property
    def robots_blue(self) -> list[DetectionRobot]:
        """robots_blue

        Returns:
            list[DetectionRobot]: The list of blue detected robots.
        """
        return self.__robots_blue
