#!/usr/bin/env python3.10

"""status_receiver.py

    This module is for the StatusReceiver class.
"""
import socket
import struct
from logging import getLogger

from racoon_ai.models.network import BUFFSIZE, Network
from racoon_ai.proto.pb_gen.grSim_Robotstatus_pb2 import Robots_Status


class StatusReceiver(Network):
    """StatusReceiver

    Args:
        host (str): The IP address of the server.
            Defaults to `224.5.23.2`
        port (int): The port to listen on.
            Defaults to `30011`
    """

    def __init__(self, *, host: str = "224.5.23.2", port: int = 30011) -> None:

        super().__init__(port, address=host)

        self.__logger = getLogger(__name__)

        # self.__robots_status: Optional[Robots_Status] = None
        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        mreq = struct.pack("4sl", socket.inet_aton(self.address), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.__sock.bind((self.address, port))

        self.__infrared: list[bool] = [False] * 16

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__sock.close()
        self.__logger.info("Socket closed")

    def receive(self) -> None:
        """recieve

        Recieve the status from the robots.

        Return:
            None
        """
        packet: bytes = self.__sock.recv(BUFFSIZE)

        robotsstatus = Robots_Status()

        robotsstatus.ParseFromString(packet)

        for robot in robotsstatus.robots_status:
            if robot.infrared:
                self.__infrared[robot.robot_id] = True
            else:
                self.__infrared[robot.robot_id] = False

    def get_infrared(self, robot_id: int) -> bool:
        """getInfrared

        Return Robots Infrared Sensor Status

        Return:
            Bool
        """
        # print(self.__infrared)
        return self.__infrared[robot_id]
