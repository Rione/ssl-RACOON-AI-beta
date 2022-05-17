#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

import math
from logging import getLogger

from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.models.coordinate import Point
from racoon_ai.networks.receiver.mw_receiver import MWReceiver


class Role:
    """Role
    Args:
        observer (Observer): Observer instance.

    Attributes:
        keeper_id (int): Keeper robot id.
        offense_ids (list[int]): Offensive robots id.
        defense_ids (list[int]): Defensive robots id.
    """

    def __init__(self, observer: MWReceiver) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        # self.__pass: int = 0
        # self.__pass_receive: int = 0
        self.__keeper: int = 0
        self.__offense: list[int] = []
        self.__defense: list[int] = []
        # self.__keeper_quantity: int = 0
        self.__offense_quantity: int = 0
        self.__defence_quantity: int = 0
        # self.__midfielder_quantity: int = 0
        self.__role_num: list[list[int]] = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 1, 0],
            [1, 1, 2, 0],
            [1, 2, 2, 0],
            [1, 2, 3, 0],
            [1, 3, 3, 0],
            [1, 3, 3, 1],
            [1, 3, 4, 1],
            [1, 3, 5, 1],
            [1, 4, 5, 1],
            [1, 4, 5, 2],
        ]
        # self.__their_goal: Point = Point(6000, 0)
        self.__our_goal: Point = Point(-6000, 0)

    @property
    def keeper_id(self) -> int:
        """keeper"""
        return self.__keeper

    @property
    def offense_ids(self) -> list[int]:
        """offense_ids"""
        return self.__offense

    @property
    def defense_ids(self) -> list[int]:
        """defense_ids"""
        return self.__defense

    def main(self) -> None:
        """main"""
        self.__decide_quantity()
        self.__decide_keeper()
        self.__decide_defense()
        self.__decide_offense()
        self.__logger.info(self.keeper_id)
        self.__logger.info(self.offense_ids)
        self.__logger.info(self.defense_ids)

    def __decide_quantity(self) -> None:
        robot_quantity = len(self.__observer.get_our_robots())
        # self.__keeper_quantity = self.__role_num[robot_quantity][0]
        self.__offense_quantity = self.__role_num[robot_quantity][1]
        self.__defence_quantity = self.__role_num[robot_quantity][2]
        # self.__midfielder_quantity = self.__role_num[robot_quantity][3]

    def __decide_keeper(self) -> None:
        """decide_keeper"""
        self.__keeper = 0

    def __decide_defense(self) -> None:
        """decide_defense"""

        defense: list[tuple[int, float, float]]

        defense = [
            (
                robot.robot_id,
                self.__defence_basis_dis(robot.robot_id),
                radian(robot, self.__our_goal),
            )
            for robot in self.__observer.get_our_robots()
            if robot.robot_id != self.keeper_id
        ]

        if defense:
            defense.sort(reverse=False, key=lambda x: x[1])
            del defense[self.__defence_quantity :]
            defense.sort(reverse=True, key=lambda x: x[2])
        self.__defense = list(row[0] for row in defense)

    # @staticmethod
    def __defence_basis_dis(self, robot_id: int) -> float:
        """defence_basis_dis"""

        robot = self.__observer.get_our_robot(robot_id)
        theta = radian_normalize(radian(robot, self.__our_goal))
        robot_dis = distance(robot, self.__our_goal)

        if abs(theta) < math.pi / 4:
            basis_dis = robot_dis - 1200 / math.cos(theta)
        else:
            basis_dis = robot_dis - 1200 / math.sin(theta)

        return basis_dis

    def __decide_offense(self) -> None:
        """decide_offense

        オフェンスの決定を行います
        Returns:
            None
        """

        offense: list[tuple[int, float, float]]
        offense = [
            (robot.robot_id, robot.x, robot.y)
            for robot in self.__observer.get_our_robots()
            if (robot.robot_id != self.keeper_id) and (robot.robot_id not in self.defense_ids)
        ]

        if offense:
            offense.sort(reverse=True, key=lambda x: x[1])
            del offense[self.__offense_quantity :]
            offense.sort(reverse=True, key=lambda x: x[2])
        self.__offense = list(row[0] for row in offense)
