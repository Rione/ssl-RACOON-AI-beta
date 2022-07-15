#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

from logging import getLogger
from math import cos, sin

from racoon_ai.common import MathUtils as MU
from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot import Robot
from racoon_ai.observer import Observer


class Role:
    """Role
    Args:
        observer (Observer): Observer instance.
        keeper_id (int): Keeper ID.

    Attributes:
        keeper_id (int): Keeper robot id.
        offense_id_list (list[int]): Offensive robots id.
        defense_id_list (list[int]): Defensive robots id.
    """

    def __init__(self, observer: Observer, *, keeper_id: int = 0) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")
        self.__observer: Observer = observer
        # self.__pass: int = 0
        # self.__pass_receive: int = 0
        self.__keeper: int = keeper_id
        self.__offense: list[int] = []
        self.__defense: list[int] = []
        # self.__keeper_quantity: int = 0
        self.__offense_quantity: int = 0
        self.__defense_quantity: int = 0
        # self.__midfielder_quantity: int = 0
        self.__role_num: list[list[int]] = [
            [0, 0, 0, 0],  # 0
            [1, 0, 0, 0],  # 1
            [1, 1, 0, 0],  # 2
            [1, 1, 1, 0],  # 3
            [1, 1, 2, 0],  # 4
            [1, 2, 2, 0],  # 5
            [1, 2, 3, 0],  # 6
            [1, 3, 3, 0],  # 7
            [1, 3, 4, 0],  # 8
            [1, 3, 4, 1],
            [1, 3, 5, 1],
            [1, 4, 5, 1],
            [1, 4, 5, 2],
        ]
        self.__goal: Point = self.__observer.geometry.goal
        self.__their_goal: Point = self.__observer.geometry.their_goal
        self.__attack_direction: float = self.__observer.attack_direction

    @property
    def keeper_id(self) -> int:
        """keeper"""
        return self.__keeper

    @property
    def offense_id_list(self) -> list[int]:
        """offense_id_list"""
        return self.__offense

    @property
    def defense_id_list(self) -> list[int]:
        """defense_id_list"""
        return self.__defense

    @property
    def get_offense_quantity(self) -> int:
        """offense_id_list"""
        return self.__offense_quantity

    @property
    def get_defense_quantity(self) -> int:
        """defense_id_list"""
        return self.__defense_quantity

    def update(self) -> None:
        """main"""
        self.__decide_quantity()
        self.__decide_defense()
        self.__decide_offense()
        self.__logger.debug(self.keeper_id)
        self.__logger.debug(self.offense_id_list)
        self.__logger.debug(self.defense_id_list)

    def __decide_quantity(self) -> None:
        robot_quantity = self.__observer.num_of_our_robots
        # self.__keeper_quantity = self.__role_num[robot_quantity][0]
        self.__offense_quantity = self.__role_num[robot_quantity][1]
        self.__defense_quantity = self.__role_num[robot_quantity][2]
        # self.__midfielder_quantity = self.__role_num[robot_quantity][3]

    def __decide_defense(self) -> None:
        """decide_defense"""

        defense: list[tuple[int, float, float]]

        defense = [
            (
                robot.robot_id,
                self.__defence_basis_dis(robot),
                MU.radian_reduce(MU.radian(robot, self.__goal), MU.radian(self.__their_goal, self.__goal))
                * self.__attack_direction,
            )
            for robot in self.__observer.our_robots_available
            if robot.robot_id != self.keeper_id
        ]

        if defense:
            defense.sort(reverse=False, key=lambda x: x[1])
            del defense[self.__defense_quantity :]
            defense.sort(reverse=True, key=lambda x: x[2])
        self.__defense = list(row[0] for row in defense)

    def __defence_basis_dis(self, bot: Robot) -> float:
        """defence_basis_dis"""

        if not bot:
            return 1e6

        theta = MU.radian_reduce(MU.radian(bot, self.__goal), MU.radian(self.__their_goal, self.__goal))
        robot_dis = MU.distance(bot, self.__goal)

        if abs(theta) < (MU.PI / 4):
            return robot_dis - (self.__observer.geometry.goal_width / cos(theta))
        return robot_dis - abs(self.__observer.geometry.goal_width / sin(theta))
        # 上記の値が帰ってくるようになったらデバック

    def __decide_offense(self) -> None:
        """decide_offense

        オフェンスの決定を行います
        Returns:
            None
        """

        offense: list[tuple[int, float, float]]
        offense = [
            (
                robot.robot_id,
                MU.distance(robot, self.__observer.geometry.their_goal),
                MU.radian_reduce(
                    MU.radian(robot, self.__observer.geometry.their_goal), MU.radian(self.__goal, self.__their_goal)
                )
                * self.__attack_direction,
            )
            for robot in self.__observer.our_robots_available
            if (robot.robot_id != self.keeper_id) and (robot.robot_id not in self.defense_id_list)
        ]

        if offense:
            offense.sort(reverse=False, key=lambda x: x[1])
            del offense[self.__offense_quantity :]
            offense.sort(reverse=False, key=lambda x: x[2])
        self.__offense = list(row[0] for row in offense)
