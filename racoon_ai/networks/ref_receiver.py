#!/usr/bin/env python3.10

"""ref_receiver.py

    This module is for the RefReceiver class.
"""

from racoon_ai.models.network import Network


class RefReceiver(Network):
    """RefReceiver

    Args:
    """

    def __init__(self, port: int = 10003, host: str = "224.5.23.1") -> None:

        super().__init__(port, multicast_group=host)

    def __del__(self) -> None:
        pass

    def receive(self) -> None:
        """receive

        Recieve the refereee messages from the gc.

        Return:
            None
        """
        raise NotImplementedError
