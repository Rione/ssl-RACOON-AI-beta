#!/usr/bin/env python3.10

"""error.py

    This module contains:
        - SimError

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/ssl_simulation_error.proto
"""


class SimError:
    """SimError

    Errors in the simulator

    Attributes:
        code (int):
            Unique code of the error for automatic handling on client side
        message (str):
            Human readable description of the error
    """

    def __init__(self, code: str, message: str) -> None:

        self.__code: str = code

        self.__message: str = message

    @property
    def error_code(self) -> str:
        """error_code

        Returns:
            str: Unique code of the error for automatic handling on client side
        """
        return self.__code

    @property
    def error_msg(self) -> str:
        """error_msg

        Returns:
            str: Human readable description of the error
        """
        return self.__message
