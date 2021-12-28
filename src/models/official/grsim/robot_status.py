#!/usr/bin/env python3.10

"""robot_status.py

    This module contains:
        - RobotStatus
        - RobotsStatus

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Robotstatus.proto
"""


class RobotStatus:
    """RobotStatus

    Attributes:
        id (int): ID of the robot
        infrared (bool):
        flat_kick (bool):
        chip_kick (bool):
    """

    def __init__(
        self,
        id: int,
        infrared: bool,
        flat_kick: bool,
        chip_kick: bool,
    ) -> None:

        self.__id: int = id

        self.__infrared: bool = infrared

        self.__flat_kick: bool = flat_kick

        self.__chip_kick: bool = chip_kick

    @property
    def id(self) -> int:
        """id

        Returns:
            int: ID of the robot
        """
        return self.__id

    @property
    def infrared(self) -> bool:
        """infrared

        Returns:
            bool:
        """
        return self.__infrared

    @property
    def flat_kick(self) -> bool:
        """flat_kick

        Returns:
            bool:
        """
        return self.__flat_kick

    @property
    def chip_kick(self) -> bool:
        """chip_kick

        Returns:
            bool:
        """
        return self.__chip_kick


class RobotsStatus:
    """RobotsStatus

    Attributes:
        robots_status (list[RobotStatus]): List of RobotStatus
    """

    def __init__(self, robots_status: list[RobotStatus]) -> None:

        self.__robots: list[RobotStatus] = robots_status

    @property
    def robots(self) -> list[RobotStatus]:
        """robots

        Returns:
            list: List of RobotStatus
        """
        return self.__robots
