#!/usr/bin/env python3.10

"""observer.py

    This module is for the Observer class.
"""

from typing import TypeAlias

from racoon_ai.models.coordinate import Point
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


class Observer(object):
    """Observer
    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self) -> None:
        self.__ball: SSL_DetectionBall
        self.__ball_slope: float = 0.00
        self.__ball_intercept: float = 0.00
        self.__pre_ball = Point(0, 0, 0)

    def vision_receiver(self, vision: VisionReceiver) -> None:
        """vision_receiver

        update vision

        Return:
            None
        """
        self.__ball = vision.ball

    def ball_status(self) -> None:
        """ball_status

        calculate ball info

        Return:
            None
        """
        ball_difference_x = self.__ball.x - self.__pre_ball.x
        ball_difference_y = self.__ball.y - self.__pre_ball.y

        if ball_difference_x != 0 and ball_difference_y != 0:
            self.__ball_slope = ball_difference_y / ball_difference_x
            # self.__ball_slope_radian = math.atan2(ball_difference_y, ball_difference_x)
            self.__ball_intercept = self.__ball.y - (self.__ball_slope * self.__ball.x)
            # self.ball_speed = math.sqrt(math.pow(ball_difference_x, 2) + math.pow(ball_difference_y, 2)) / 0.016

        self.__pre_ball.x = self.__ball.x
        self.__pre_ball.y = self.__ball.y

    def get_ball_slope(self) -> float:
        """
        Returns:
            float: ball_slope
        """
        return self.__ball_slope

    def get_ball_intercept(self) -> float:
        """
        Returns:
            float: ball_intercept
        """
        return self.__ball_intercept
