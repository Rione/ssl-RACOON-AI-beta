#!/usr/bin/env python3.10

"""observer.py

    This module is for the Observer class.
"""
import math
from logging import getLogger

from racoon_ai import common
from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot import RobotCommand
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot


class Observer:
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
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__ball: SSL_DetectionBall
        self.__ball_slope: float = 0.00
        self.__ball_intercept: float = 0.00
        self.__pre_ball = Point(0, 0, 0)
        self.__their_robots: list[SSL_DetectionRobot]

    def vision_receiver(self, vision: VisionReceiver) -> None:
        """vision_receiver

        update vision

        Return:
            None
        """
        self.__ball = vision.get_ball()
        self.__their_robots = vision.yellow_robots

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

    def _avoid_collision(self, robot: SSL_DetectionRobot, command: RobotCommand, target_radian: float) -> RobotCommand:
        nearest_robot, min_distance, min_radian = self._detection_near_robot(robot)

        if min_distance < 380 and ((min_radian > 0 and target_radian > 0) or (min_radian < 0 and target_radian < 0)):
            for robot_their in range(4):
                if self.__their_robots[robot_their].robot_id == nearest_robot:
                    degree_invasion = common.radian(self.__their_robots[robot_their], robot) - robot.orientation
                    if degree_invasion > 0:
                        avoid_degree = degree_invasion + math.pi / 2
                        command.vel_fwd = math.cos(avoid_degree) * 0.25
                        command.vel_sway = math.sin(avoid_degree) * 0.25
                    else:
                        avoid_degree = degree_invasion - math.pi / 2
                        command.vel_fwd = math.cos(avoid_degree - math.pi) * 0.25
                        command.vel_sway = math.sin(avoid_degree - math.pi) * 0.25

        return command

    def _detection_near_robot(self, robot: SSL_DetectionRobot) -> tuple[int, float, float]:
        min_robot_id = -1
        min_distance = 10000000.0
        min_radian = 0.0
        for robot_their in range(4):
            if robot.robot_id == 0 and self.__their_robots[robot_their].robot_id == 3:
                min_robot_id = 3
                min_radian = common.radian_normalize(
                    common.radian(self.__their_robots[robot_their], robot) - robot.orientation
                )
                min_distance = common.distance(self.__their_robots[robot_their], robot)
            elif robot.robot_id == 1 and self.__their_robots[robot_their].robot_id == 4:
                min_robot_id = 4
                min_radian = common.radian_normalize(
                    common.radian(self.__their_robots[robot_their], robot) - robot.orientation
                )
                min_distance = common.distance(self.__their_robots[robot_their], robot)

        return min_robot_id, min_distance, min_radian

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
