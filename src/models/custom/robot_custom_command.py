#!/usr/bin/env python3.10


class RobotCustomCommand:
    def __init__(self):

        self.__is_emergency_pressed: bool = False

    def __str__(self) -> str:
        return f"EmergencyPressed: {self.__is_emergency_pressed}"
