#!/usr/bin/env python3.10

"""mw_receiver.py

    This module is for the MwReceiver class.
"""

from logging import getLogger
from socket import AF_INET, IPPROTO_UDP, SO_REUSEADDR, SOCK_DGRAM, SOL_SOCKET, socket

from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import RacoonMW_Packet


class MWReceiver(IPNetAddr):  # pylint: disable=R0904
    """VisionReceiver

    Args:
        target_ids (list[int]): Target robot IDs
        is_real (bool): True if the receiver is for real robot (default: False)
        is_team_yellow (bool, optional): If true, the team is yellow (default: False)
        host (str, optional): IP or hostname of the server
        port (int, optional): Port number of the vision server
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 30011) -> None:

        super().__init__(host, port)

        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")

        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__sock.close()
        self.__logger.info("Socket closed")

    def recv(self) -> RacoonMW_Packet:
        """recv"""
        packet: bytes = self.__sock.recv(BUFFSIZE)
        proto = RacoonMW_Packet()
        proto.ParseFromString(packet)
        self.__logger.debug("Received %s", proto)
        return proto
