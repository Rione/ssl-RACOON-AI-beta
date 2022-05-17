#!/usr/bin/env python3.10

"""observer.py

    This module contains
        - Observer
"""

from logging import getLogger
from time import time

from racoon_ai.models.ball import Ball
from racoon_ai.models.robot import Robot
from racoon_ai.networks.receiver import VisionReceiver


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
        return self.__yellow_robots if self.is_team_yellow else self.__blue_robots

    @property
    def their_robots(self) -> list[Robot]:
        """their_robots"""
        return self.__blue_robots if self.is_team_yellow else self.__yellow_robots

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
