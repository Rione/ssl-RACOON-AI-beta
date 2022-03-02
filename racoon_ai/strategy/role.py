#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

from logging import getLogger

from racoon_ai.observer import Observer


class Role:
    """Role
    Args:
        observer (Observer): Observer instance.

    Attributes:
        keeper_id (int): Keeper robot id.
        offense_ids (list[int]): Offensive robots id.
        defense_ids (list[int]): Defensive robots id.
    """

    def __init__(self, observer: Observer, offe_cnt: int = 3, def_cnt: int = 3) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")

        self.__observer = observer
        # self.__pass: int = 0
        # self.__pass_receive: int = 0
        self.__keeper: int = 0
        self.__offense: list[int] = []
        self.__defense: list[int] = []
        self.__offense_quantity: int = offe_cnt
        self.__defence_quantity: int = def_cnt

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
        self.__decide_keeper()
        self.__decide_defense()
        self.__decide_offense()
        self.__logger.debug(self.keeper_id)
        self.__logger.info(self.offense_ids)
        self.__logger.debug(self.defense_ids)

    def __decide_keeper(self) -> None:
        """decide_keeper"""
        self.__keeper = 0

    def __decide_defense(self) -> None:
        """decide_defense"""

        defense: list[tuple[int, float, float]]
        defense = [
            (robot.robot_id, robot.x, robot.y)
            for robot in self.__observer.our_robots
            if robot.robot_id != self.keeper_id
        ]

        if defense:
            defense.sort(reverse=False, key=lambda x: x[1])
            del defense[self.__defence_quantity :]
            defense.sort(reverse=True, key=lambda x: x[2])
        self.__defense = list(set(row[0] for row in defense))

    def __decide_offense(self) -> None:
        """decide_offense

        オフェンスの決定を行います
        Returns:
            None
        """

        offense: list[tuple[int, float, float]]
        offense = [
            (robot.robot_id, robot.x, robot.y)
            for robot in self.__observer.our_robots
            if (robot.robot_id != self.keeper_id) and (robot.robot_id not in self.defense_ids)
        ]

        if offense:
            offense.sort(reverse=False, key=lambda x: x[1])
            del offense[self.__offense_quantity :]
            offense.sort(reverse=True, key=lambda x: x[2])
        self.__offense = list(set(row[0] for row in offense))
