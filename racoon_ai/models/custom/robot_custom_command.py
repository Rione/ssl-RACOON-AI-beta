#!/usr/bin/env python3.10

""" robot_custom_command.py

    This module contains:
        - RobotCustomCommand
"""


class RobotCustomCommand:
    """RobotCustomCommand

    A custom command for our robots.

    Attributes:
        is_emergency_pressed (bool): True if the emergency button is pressed.
    """

    def __init__(self):

        self.__is_emergency_pressed: bool = False

    def __str__(self) -> str:
        return (
            "RobotCustomCommand("
            f"is_emergency_pressed={self.is_emergency_pressed}"
            ")"
        )

    @property
    def is_emergency_pressed(self) -> bool:
        """is_emergency_pressed

        Return:
            bool: True if the emergency button is pressed.
        """
        return self.__is_emergency_pressed

    @is_emergency_pressed.setter
    def is_emergency_pressed(self, value: bool):
        """is_emergency_pressed

        Args:
            value (bool): True if the emergency button is pressed.
        """
        self.__is_emergency_pressed = value


if __name__ == "__main__":
    custom_cmd = RobotCustomCommand()
    print(custom_cmd)
