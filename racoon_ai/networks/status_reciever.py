#!/usr/bin/env python3.10

"""status_receiver.py

    This module is for the StatusReceiver class.
"""

from racoon_ai.models.network import Network


class StatusReceiver(Network):
    """StatusReceiver

    Args:
        port (int): The port to listen on.
    """

    def __init__(self, port: int = 30011) -> None:

        super().__init__(port)

    def __del__(self) -> None:
        pass

    def recieve(self) -> None:
        """recieve

        Recieve the status from the robots.

        Return:
            None
        """
        raise NotImplementedError
