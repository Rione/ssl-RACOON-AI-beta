#!/usr/bin/env python3.10

"""robot_command.py

    This module is for the RobotCommand class.
"""


class RobotCommand:
    """RobotCommand

    Args:
        id (int): ID of the robot
        kickspeedx (float): Kick speed in x direction
        kickspeedz (float): Kick speed in z direction
        veltangent (float): Velocity in the tangent direction
        velnormal (float): Velocity in the normal direction
        velangular (float): Velocity in the angular direction
        spinner (bool): Whether the dribller spins or not
        wheelsspeed (bool): Whether control by the each wheels or not
        wheel1 (float): Speed of the first wheel
        wheel2 (float): Speed of the second wheel
        wheel3 (float): Speed of the third wheel
        wheel4 (float): Speed of the fourth wheel
    """

    def __init__(
        self,
        id: int,
        kickspeedx: float,
        kickspeedz: float,
        veltangent: float,
        velnormal: float,
        velangular: float,
        spinner: bool,
        wheelsspeed: bool,
        wheel1: float,
        wheel2: float,
        wheel3: float,
        wheel4: float,
    ):

        self.__id: int = id

        self.__kickspeedx: float = kickspeedx

        self.__kickspeedz: float = kickspeedz

        self.__veltangent: float = veltangent

        self.__velnormal: float = velnormal

        self.__velangular: float = velangular

        self.__spinner: bool = spinner

        self.__wheelsspeed: bool = wheelsspeed

        self.__wheel1: float = wheel1

        self.__wheel2: float = wheel2

        self.__wheel3: float = wheel3

        self.__wheel4: float = wheel4

    def __str__(self) -> str:
        pass

    @property
    def id(self) -> int:
        """id

        Returns:
            int: ID of the robot
        """
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        """id

        Args:
            value (int): ID of the robot
        """
        self.__id = value

    @property
    def kickspeedx(self) -> float:
        """kickspeedx

        Returns:
            float: Kick speed in x direction
        """
        return self.__kickspeedx

    @kickspeedx.setter
    def kickspeedx(self, value: float) -> None:
        self.__kickspeedx = value

    @property
    def kickspeedz(self) -> float:
        """kickspeedz

        Returns:
            float: Kick speed in z direction
        """
        return self.__kickspeedz

    @kickspeedz.setter
    def kickspeedz(self, value: float) -> None:
        """kickspeedz

        Args:
            value (float): Kick speed in z direction
        """
        self.__kickspeedz = value

    @property
    def veltangent(self) -> float:
        """veltangent

        Returns:
            float: Velocity in the tangent direction
        """
        return self.__veltangent

    @veltangent.setter
    def veltangent(self, value: float) -> None:
        """veltangent

        Args:
            value (float): Velocity in the tangent direction
        """
        self.__veltangent = value

    @property
    def velnormal(self) -> float:
        """velnormal

        Returns:
            float: Velocity in the normal direction
        """
        return self.__velnormal

    @velnormal.setter
    def velnormal(self, value: float) -> None:
        """velnormal

        Args:
            value (float): Velocity in the normal direction
        """
        self.__velnormal = value

    @property
    def velangular(self) -> float:
        """velangular

        Returns:
            float: Velocity in the angular direction
        """
        return self.__velangular

    @velangular.setter
    def velangular(self, value: float) -> None:
        """velangular

        Args:
            value (float): Velocity in the angular direction
        """
        self.__velangular = value

    @property
    def spinner(self) -> bool:
        """spinner

        Returns:
            bool: Whether the dribller spins or not
        """
        return self.__spinner

    @spinner.setter
    def spinner(self, value: bool) -> None:
        """spinner

        Args:
            value (bool): Whether the dribller spins or not
        """
        self.__spinner = value

    @property
    def wheelsspeed(self) -> bool:
        """wheelsspeed

        Returns:
            bool: Whether control by the each wheels or not
        """
        return self.__wheelsspeed

    @wheelsspeed.setter
    def wheelsspeed(self, value: bool) -> None:
        """wheelsspeed

        Args:
            value (bool): Whether control by the each wheels or not
        """
        self.__wheelsspeed = value

    @property
    def wheel1(self) -> float:
        """wheel1

        Returns:
            float: Speed of the first wheel
        """
        return self.__wheel1

    @wheel1.setter
    def wheel1(self, value: float) -> None:
        """wheel1

        Args:
            value (float): Speed of the first wheel
        """
        self.__wheel1 = value

    @property
    def wheel2(self) -> float:
        """wheel2

        Returns:
            float: Speed of the second wheel
        """
        return self.__wheel2

    @wheel2.setter
    def wheel2(self, value: float) -> None:
        """wheel2

        Args:
            value (float): Speed of the second wheel
        """
        self.__wheel2 = value

    @property
    def wheel3(self) -> float:
        """wheel3

        Returns:
            float: Speed of the third wheel
        """
        return self.__wheel3

    @wheel3.setter
    def wheel3(self, value: float) -> None:
        """wheel3

        Args:
            value (float): Speed of the third wheel
        """
        self.__wheel3 = value

    @property
    def wheel4(self) -> float:
        """wheel4

        Returns:
            float: Speed of the fourth wheel
        """
        return self.__wheel4

    @wheel4.setter
    def wheel4(self, value: float) -> None:
        """wheel4

        Args:
            value (float): Speed of the fourth wheel
        """
        self.__wheel4 = value
