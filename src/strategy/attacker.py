#!/usr/bin/env python3.10

"""attacker.py

    This module is for the Attacker class.
"""

from models.official.grsim.commands import RobotCommand


class Attacker(object):
    def __init__(self, vision):
        self.__vision = vision
        self.__attacker_id = 0
        self.__kickspeedx = 0
        self.__kickspeedz = 0
        self.__veltangent = 0
        self.__velnormal = 3.9
        self.__velangular = 0
        self.__spinner = 0

    def some_logics(self):
        pass

    def send_command(self):
        send_command = RobotCommand(
            self.__attacker_id,
            self.__kickspeedx,
            self.__kickspeedz,
            self.__veltangent,
            self.__velnormal,
            self.__velangular,
            self.__spinner,
            False,
            0,
            0,
            0,
            0,
        )

        return send_command
