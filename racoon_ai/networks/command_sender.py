#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

import socket
import time
from typing import List

from racoon_ai.models.grsim.commands import RobotCommand
from racoon_ai.proto_py.grSim_Commands_pb2 import grSim_Commands, grSim_Robot_Command
from racoon_ai.proto_py.grSim_Packet_pb2 import grSim_Packet


class CommandSender:
    """CommandSender

    Args:
        is_yellow (bool): True if the robot is yellow.
    """

    def __init__(self, is_yellow: bool = False):

        self.__port = 20011

        self.__multicast_group = "127.0.0.1"

        self.__data: List[RobotCommand] = []

        self.__is_yellow = is_yellow

        # ˅
        self.__local_address = "0.0.0.0"

        # 送信ソケット作成
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_MULTICAST_IF,
            socket.inet_aton(self.__local_address),
        )

    def send(self):
        """
        送信実行
        :return: None
        """
        # タイムスタンプ等、grSimCommandsに必要な要素を用意
        timestamp = time.time()
        isteamyellow = self.__is_yellow

        send_data = grSim_Commands()

        # set_robotcommandされた分だけループさせる
        # TO_DO: 複数同じロボットがappendされてたらどうする？
        for robot_command in self.__data:
            send_data_one: grSim_Robot_Command = grSim_Robot_Command()
            send_data_one.id = robot_command.robot_id
            send_data_one.kickspeedx = robot_command.kickpow
            send_data_one.kickspeedz = robot_command.kickpow_z
            send_data_one.veltangent = robot_command.vel_fwd
            send_data_one.velnormal = robot_command.vel_sway
            send_data_one.velangular = robot_command.vel_angular
            send_data_one.spinner = bool(robot_command.dribble_pow)
            send_data_one.wheelsspeed = robot_command.use_wheels_speed

            if robot_command.use_wheels_speed:
                send_data_one.wheel1 = robot_command.wheel1
                send_data_one.wheel2 = robot_command.wheel2
                send_data_one.wheel3 = robot_command.wheel3
                send_data_one.wheel4 = robot_command.wheel4

            send_data.robot_commands.append(send_data_one)

        send_data.timestamp = timestamp
        send_data.isteamyellow = isteamyellow

        send_packet = grSim_Packet()
        send_packet.commands.CopyFrom(send_data)
        send_packet = send_packet.SerializeToString()

        # 送信する
        self.__sock.sendto(send_packet, (self.__multicast_group, self.__port))

    def set_robotcommand(self, robotcommand):
        """
        ロボットコマンドを追加
        :param robotcommand: RobotCommandの型が入ります
        :return: None
        """
        # self.__dataに追加していく
        self.__data.append(robotcommand)
