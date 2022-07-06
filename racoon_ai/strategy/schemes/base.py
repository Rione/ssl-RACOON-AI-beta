#!/usr/bin/env python3.10

"""base.py

    This module contains:
        - StrategyBase
"""

from logging import getLogger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from ..role import Role


class StrategyBase:
    """StrategyBase

    Args:
        observer (Observer): Observer instance
        controls (Controls): Controls instance
        role (Role): Role instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, controls: Controls, role: Role) -> None:

        getLogger(__name__).debug("Initializing...")

        self.__observer: Observer = observer

        self.__controls: Controls = controls

        self.__role: Role = role

        self.__send_cmds: list[RobotCommand] = []

    @property
    def observer(self) -> Observer:
        """observer

        Returns:
            Observer
        """
        return self.__observer

    @property
    def controls(self) -> Controls:
        """controls

        Returns:
            Controls
        """
        return self.__controls

    @property
    def role(self) -> Role:
        """role

        Returns:
            Role
        """
        return self.__role

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]
        """
        return self.__send_cmds

    @send_cmds.setter
    def send_cmds(self, cmds: list[RobotCommand]) -> None:
        """send_cmds

        Args:
            cmds (list[RobotCommand]): RobotCommand list.
        """
        self.__send_cmds = cmds
