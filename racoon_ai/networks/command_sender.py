#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

import socket
from logging import getLogger

from racoon_ai.models.network import Network
from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Commands
from racoon_ai.proto.pb_gen.grSim_Packet_pb2 import grSim_Packet


class CommandSender(Network):
    """CommandSender

    Args:
        is_yellow (bool): True if the robot is yellow.
    """

    def __init__(self, port: int = 20011) -> None:

        super().__init__(port)

        self.__logger = getLogger(__name__)

        # 送信ソケット作成
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__sock.close()
        self.__logger.info("Socket closed")

    def send(self, sim_cmds: SimCommands, online_id: list[int], real_mode: bool) -> None:
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

        # self.__sock.sendto(packet, (self.multicast_group, self.port))

        # FOR REAL ENVIROMENT
        # 実機環境
        if real_mode:
            for i in sim_cmds.robot_commands:
                robotip: int = 100 + i.robot_id
                if i.robot_id in online_id:
                    try:
                        # 192.168.100.1xx: xxにはロボットIDが入る。
                        # そのIPに送信している
                        self.__sock.sendto(packet, ("192.168.100." + str(robotip), self.port))

                    except OSError:
                        # オンラインじゃないIPアドレスに送信するとOSエラーが返ってくるのでキャッチする
                        print("OSError: Host " + "192.168.100." + str(robotip) + " is down!")
        else:
            # CHANGE SEND IP
            # grSimに合うよう変更してください
            self.__sock.sendto(packet, ("localhost", self.port))

    def stop_robots(self, online_id: list[int], real_mode: bool) -> None:
        """
        Returns:
            Simcommands: commands
        """

        for _ in range(10):
            commands = SimCommands()
            for robot in range(11):
                command = RobotCommand(robot)
                command.vel_fwd = 0
                command.vel_sway = 0
                command.vel_angular = 0
                command.kickpow = 0
                command.dribble_pow = 0

                commands.robot_commands.append(command)
            self.send(commands, online_id, real_mode)
