#!/usr/bin/env python3.10

"""strategy.py

    This module contains:
        - Strategy
"""

from logging import Logger, getLogger

from racoon_ai.movement import Controls
from racoon_ai.observer import Observer
from racoon_ai.strategy.role import Role, SubRole

from .schemes import Defense, Keeper, Offense, OutOfPlay


class Strategy:
    """Strategy

    Wrapper class for strategy schemes.

    """

    def __init__(self, observer: Observer, role: Role, controls: Controls) -> None:

        self.__logger: Logger = getLogger(__name__)
        self.__logger.debug("Initializing...")

        self.__controls: Controls = controls

        self.__subrole: SubRole = SubRole(observer, role)

        self.__defense: Defense = Defense(observer, role, self.__subrole, controls)

        self.__keeper: Keeper = Keeper(observer, role, controls)

        self.__offense: Offense = Offense(observer, role, self.__subrole, controls)

        self.__out_of_play: OutOfPlay = OutOfPlay(observer, role, self.__subrole, controls)

    @property
    def controls(self) -> Controls:
        """controls"""
        return self.__controls

    @property
    def subrole(self) -> SubRole:
        """subrole"""
        return self.__subrole

    @property
    def defense(self) -> Defense:
        """defense"""
        return self.__defense

    @property
    def keeper(self) -> Keeper:
        """keeper"""
        return self.__keeper

    @property
    def offense(self) -> Offense:
        """offense"""
        return self.__offense

    @property
    def out_of_play(self) -> OutOfPlay:
        """out_of_play"""
        return self.__out_of_play
