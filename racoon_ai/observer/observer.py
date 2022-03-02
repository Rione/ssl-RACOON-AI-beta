#!/usr/bin/env python3.10

"""observer.py

    This module contains
        - Observer
"""

from logging import getLogger
from time import time

from racoon_ai.models.ball import Ball
from racoon_ai.models.robot import Robot
from racoon_ai.networks.reciever import VisionReceiver


class Observer:
    """Observer

    Wrapper for receivers

    Attributes:
        ball (Ball): State of the most recent ball
        is_team_yellow (bool): Whether the team is yellow
        our_robots (List[Robot]): State of the most recent robots
        their_robots (List[Robot]): State of the most recent robots
    """

    def __init__(self, vision: VisionReceiver, is_team_yellow: bool = False) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")

        self.__vision: VisionReceiver = vision
        self.__ball: Ball = Ball()
        self.__is_team_yellow: bool = is_team_yellow
        self.__blue_robots: list[Robot] = [Robot(i) for i in range(11)]
        self.__yellow_robots: list[Robot] = [Robot(i) for i in range(11)]

    @property
    def ball(self) -> Ball:
        """ball"""
        return self.__ball

    @property
    def is_team_yellow(self) -> bool:
        """is_team_yellow"""
        return self.__is_team_yellow

    @property
    def our_robots(self) -> list[Robot]:
        """our_robots"""
        if self.is_team_yellow:
            return self.__yellow_robots
        return self.__blue_robots

    @property
    def their_robots(self) -> list[Robot]:
        """their_robots"""
        if self.is_team_yellow:
            return self.__blue_robots
        return self.__yellow_robots

    def main(self) -> None:
        """main"""
        self.__vision.main()
        curr: float = time()
        self.__update_ball_state(curr)
        self.__update_robot_state(curr)

    def __update_ball_state(self, timestamp: float) -> None:
        """update_ball_state"""
        if self.__vision.balls:
            self.ball.update(self.__vision.balls[0], timestamp)
            self.__logger.debug(self.ball)

    def __update_robot_state(self, timestamp: float) -> None:
        """update_robot_state"""

        bot: Robot
        for dbot in self.__vision.blue_robots:
            bot = self.__blue_robots[dbot.robot_id]
            if timestamp - bot.timestamp < 1e-3:
                continue
            bot.update(dbot, timestamp)

        for dbot in self.__vision.yellow_robots:
            bot = self.__yellow_robots[dbot.robot_id]
            if timestamp - bot.timestamp < 1e-3:
                continue
            bot.update(dbot, timestamp)

    # def _update_ball(self) -> None:
    #     """

    #     calculate ball info

    #     Return:
    #         None
    #     """
    #     if not self.ball:
    #         return

    #     ball_delta_x = self.ball.x
    #     ball_delta_y = self.ball.y

    #     if self.prev_ball:
    #         ball_delta_x -= self.prev_ball.x
    #         ball_delta_y -= self.prev_ball.y

    #     if ball_delta_x != 0 and ball_delta_y != 0:
    #         self.__ball_slope = ball_delta_y / ball_delta_x
    #         # self.__ball_slope_radian = math.atan2(ball_difference_y, ball_difference_x)
    #         self.__ball_intercept = self.ball.y - (self.__ball_slope * self.ball.x)
    #         # self.ball_speed = math.sqrt(math.pow(ball_difference_x, 2) + math.pow(ball_difference_y, 2)) / 0.016
    #     self.__prev_ball = self.ball

    # def _avoid_collision(
    #   self,
    #   robot: SSL_DetectionRobot,
    #   command: RobotCommand,
    #   target_radian: float,
    # ) -> RobotCommand:
    #     nearest_robot, min_distance, min_radian = self._detection_near_robot(robot)

    #     if min_distance < 380 and ((min_radian > 0 and target_radian > 0) or (min_radian < 0 and target_radian < 0)):
    #         for robot_their in range(4):
    #             if self.__their_robots[robot_their].robot_id == nearest_robot:
    #                 degree_invasion = common.radian(self.__their_robots[robot_their], robot) - robot.orientation
    #                 if degree_invasion > 0:
    #                     avoid_degree = degree_invasion + math.pi / 2
    #                     command.vel_fwd = math.cos(avoid_degree) * 0.25
    #                     command.vel_sway = math.sin(avoid_degree) * 0.25
    #                 else:
    #                     avoid_degree = degree_invasion - math.pi / 2
    #                     command.vel_fwd = math.cos(avoid_degree - math.pi) * 0.25
    #                     command.vel_sway = math.sin(avoid_degree - math.pi) * 0.25

    #     return command

    # def _detection_near_robot(self, robot: SSL_DetectionRobot) -> tuple[int, float, float]:
    #     min_robot_id = -1
    #     min_distance = 10000000.0
    #     min_radian = 0.0
    #     for robot_their in range(4):
    #         if robot.robot_id == 0 and self.__their_robots[robot_their].robot_id == 3:
    #             min_robot_id = 3
    #             min_radian = common.radian_normalize(
    #                 common.radian(self.__their_robots[robot_their], robot) - robot.orientation
    #             )
    #             min_distance = common.distance(self.__their_robots[robot_their], robot)
    #         elif robot.robot_id == 1 and self.__their_robots[robot_their].robot_id == 4:
    #             min_robot_id = 4
    #             min_radian = common.radian_normalize(
    #                 common.radian(self.__their_robots[robot_their], robot) - robot.orientation
    #             )
    #             min_distance = common.distance(self.__their_robots[robot_their], robot)

    #     return min_robot_id, min_distance, min_radian
