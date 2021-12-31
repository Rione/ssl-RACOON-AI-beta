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

    def __str__(self) -> str:
        return (
            "RobotStatus("
            f"id={self.id:2d}, "
            f"infrared={self.infrared!s}, "
            f"flat_kick={self.flat_kick!s}, "
            f"chip_kick={self.chip_kick!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "RobotStatus("
            f"{self.id}, "
            f"{self.infrared}, "
            f"{self.flat_kick}, "
            f"{self.chip_kick}"
            ")"
        )

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

    def __str__(self) -> str:
        return f"RobotsStatus(robots={self.robots!s})"

    def __repr__(self) -> str:
        return f"RobotsStatus({self.robots})"

    @property
    def robots(self) -> list[RobotStatus]:
        """robots

        Returns:
            list: List of RobotStatus
        """
        return self.__robots
