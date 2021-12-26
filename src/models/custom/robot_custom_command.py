#!/usr/bin/env python3.10

""" robot_custom_command.py

    This module contains the RobotCustomCommand class.
"""


class RobotCustomCommand:
    """RobotCustomCommand

    A custom command for our robots.

    Attributes:
        is_emergency_pressed (bool): True if the emergency button is pressed.
    """

    def __init__(self):

        self.is_emergency_pressed: bool = False

    def __str__(self) -> str:
        pass
