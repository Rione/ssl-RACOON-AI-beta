#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

import time
import socket

from models.official.grsim.commands import SimRobotCommand
from proto_py.grSim_Commands_pb2 import grSim_Robot_Command
from proto_py.grSim_Commands_pb2 import grSim_Commands
from proto_py.grSim_Packet_pb2 import grSim_Packet


class CommandSender(object):
    """CommandSender

    Args:
        is_yellow (bool): True if the robot is yellow.
    """

    def __init__(self, is_yellow: bool = False):

        self.__port = 20011

        self.__multicast_group = "127.0.0.1"

        self.__data = []

        self.__is_yellow = is_yellow

        # ˅
        self.__local_address = "0.0.0.0"

        # 送信ソケット作成
        self.__sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
        )
        self.__sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(self.__local_address),
        )

    def send(self):
        # タイムスタンプ等、grSimCommandsに必要な要素を用意
        timestamp = time.time()
        isteamyellow = self.__is_yellow

        send_data = grSim_Commands()

        # set_robotcommandされた分だけループさせる
        # TODO: 複数同じロボットがappendされてたらどうする？
        for robot_command in self.__data:
            send_data_one = grSim_Robot_Command()
            send_data_one.id = robot_command.id
            send_data_one.kickspeedx = robot_command.kickspeedx
            send_data_one.kickspeedz = robot_command.kickspeedz
            send_data_one.veltangent = robot_command.veltangent
            send_data_one.velnormal = robot_command.velnormal
            send_data_one.velangular = robot_command.velangular
            send_data_one.spinner = robot_command.spinner
            send_data_one.wheelsspeed = robot_command.wheelsspeed

            send_data.robot_commands.append(send_data_one)

        send_data.timestamp = timestamp
        send_data.isteamyellow = isteamyellow

        send_packet = grSim_Packet()
        send_packet.commands.CopyFrom(send_data)
        send_packet = send_packet.SerializeToString()

        # 送信する
        self.__sock.sendto(send_packet, (self.__multicast_group, self.__port))

    def set_robotcommand(self, robotcommand):
        # self.__dataに追加していく
        self.__data.append(robotcommand)
