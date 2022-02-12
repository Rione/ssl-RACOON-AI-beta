#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

import socket

from racoon_ai.models.network import Network
from racoon_ai.models.robot.commands import SimCommands
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Commands
from racoon_ai.proto.pb_gen.grSim_Packet_pb2 import grSim_Packet


class CommandSender(Network):
    """CommandSender

    Args:
        is_yellow (bool): True if the robot is yellow.
    """

    def __init__(self, port: int = 20011) -> None:

        super().__init__(port)

        # 送信ソケット作成
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __del__(self) -> None:
        self.__sock.close()

    def send(self, sim_cmds: SimCommands) -> None:
        """
        送信実行
        :return: None
        """
        # TODO: 複数同じロボットがappendされてたらどうする？
        send_data = grSim_Commands(robot_commands=sim_cmds.to_proto())
        send_data.isteamyellow = sim_cmds.isteamyellow
        send_data.timestamp = sim_cmds.timestamp

        send_packet = grSim_Packet(commands=send_data)
        packet: bytes = send_packet.SerializeToString()

        # 送信する
        self.__sock.sendto(packet, (self.multicast_group, self.port))
