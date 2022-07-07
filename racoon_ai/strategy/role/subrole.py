#!/usr/bin/env python3.10

"""role.py
    This module is for the Role class.
"""

from logging import getLogger

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.robot import Robot
from racoon_ai.observer import Observer

from .role import Role


class SubRole:
    """SubRole
    Args:
        observer (Observer): Observer instance
        role (Role): Role instance
    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self, observer: Observer, role: Role) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing ...")

        self.__our_attacker: int = -1
        self.__enemy_attacker: int = -1
        self.__receiver: int = -1
        self.__observer: Observer = observer
        self.__role = role

    @property
    def our_attacker_id(self) -> int:
        """our_attacker_id"""
        return self.__our_attacker

    @property
    def enemy_attacker_id(self) -> int:
        """enemy_attacker_id"""
        return self.__enemy_attacker

    @property
    def receiver_id(self) -> int:
        """receiver_id"""
        return self.__receiver

    def main(self) -> None:
        """main
        Returns:
            None
        """
        self.decide_our_attacker()
        self.decide_enemy_attacker()
        self.decide_receiver()
        self.__logger.debug(self.__our_attacker)
        self.__logger.debug(self.__receiver)

    def decide_our_attacker(self) -> None:
        """decide_our_attacker
        Returns:
           None
        """
        attacker: list[tuple[int, float]]
        attacker = [
            (
                robot.robot_id,
                MU.distance(self.__observer.ball, robot),
            )
            for robot in self.__observer.our_robots
            if robot.robot_id != self.__role.keeper_id
            and robot.robot_id not in self.__role.defense_id_list
            and robot.is_visible is True
        ]
        if attacker:
            attacker.sort(reverse=False, key=lambda x: x[1])
            self.__our_attacker = int(attacker[0][0])

    def decide_enemy_attacker(self) -> None:
        """decide_their_attacker
        Returns:
           None
        """
        attacker: list[tuple[int, float]]
        attacker = [
            (
                enemy.robot_id,
                MU.distance(self.__observer.ball, enemy),
            )
            for enemy in self.__observer.enemy_robots
            if enemy.is_visible is True
        ]
        if attacker:
            attacker.sort(reverse=False, key=lambda x: x[1])
            self.__enemy_attacker = int(attacker[0][0])

    def decide_receiver(self) -> None:
        """decide_receiver
        Return:
          None
        """
        receiver: list[tuple[int, float]]
        attacker: Robot = self.__observer.our_robots[self.__our_attacker]
        receiver = [
            (
                robot.robot_id,
                MU.distance(robot, attacker),
            )
            for robot in self.__observer.our_robots
            if robot.robot_id not in (self.__role.keeper_id, self.__our_attacker, self.__role.defense_id_list)
            and robot.is_visible is True
        ]

        if receiver:
            receiver.sort(reverse=False, key=lambda x: x[1])
            self.__receiver = int(receiver[0][0])
