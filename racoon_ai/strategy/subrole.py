#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

from racoon_ai.common import distance
from racoon_ai.observer import Observer
from racoon_ai.strategy.offense import Offense


class SubRole:
    """SubRole
    Args:
        observer (Observer): Observer instance.

    Attributes:
        pass_provider_id (int): pass provider id.
        pass_receiver_id (int): pass receiver id.

    """

    def __init__(self, observer: Observer) -> None:
        self.__pass_provider: int = 0
        self.__pass_receive: int = 0
        self.__observer: Observer = observer
        self.__offense: Offense

    @property
    def pass_provider_id(self) -> int:
        """pass_provider_id

        Returns:
            int: pass provider id
        """
        return self.__pass_provider

    @property
    def pass_reciever_id(self) -> int:
        """pass_reciever_id

        Returns:
            int: pass reciever id
        """
        return self.__pass_receive

    def main(self) -> None:
        """main"""
        self.__decide_pass_provider()
        self.__decide_pass_receive()

    def __decide_pass_provider(self) -> None:
        """decide_pass_provider"""
        if self.__offense.kick_flag is False:
            min_distance = 10000000.0
            self.__pass_provider = -1
            for robot in self.__observer.our_robots:
                distance_robot_ball = distance(robot, self.__observer.ball)
                if distance_robot_ball < min_distance:
                    min_distance = distance_robot_ball
                    self.__pass_provider = robot.robot_id

    def __decide_pass_receive(self) -> None:
        """decide_pass_receive"""
        if self.pass_provider_id == 1:
            self.__pass_receive = 0
        else:
            self.__pass_receive = 1
