#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

import socket
from logging import getLogger

from racoon_ai.models.network import IPNetAddr
from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Commands
from racoon_ai.proto.pb_gen.grSim_Packet_pb2 import grSim_Packet


class CommandSender:
    """CommandSender

    Args:
        is_real (bool): If true, send commands to real robot.
        online_ids (list[int]): List of online robot ids.
        host (str, optional): IP address of the target.
            Defaults to `224.5.23.2`.
        port (int, optional): Port number of the target.
            Defaults to `20011`.

    TODO:
        Implement a method to change the address and port on the fly.
    """

    def __init__(
        self,
        is_real: bool,
        online_ids: list[int],
        *,
        host: str = "224.5.23.2",
        port: int = 20011,
    ) -> None:

        self.__logger = getLogger(__name__)

        self.__is_real: bool = is_real

        self.__online_ids: list[int] = online_ids

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        self.__dists: list[IPNetAddr]

        if is_real and online_ids:
            host_ips: list[str] = [f"192.168.100.1{robot_id:02d}" for robot_id in online_ids]
            self.__dists = [IPNetAddr(host, port, mod_name=__name__) for host in host_ips]
        else:
            self.__dists = [IPNetAddr(host, port, mod_name=__name__)]
            self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__stop_robots()
        self.__sock.close()
        self.__logger.info("Socket closed")

    @property
    def is_real(self) -> bool:
        """is_real

        Returns:
            bool: If true, send commands to real robot.
        """
        return self.__is_real

    @property
    def online_ids(self) -> list[int]:
        """online_ids

        List of online robot ids.

        Returns:
            list[int]: online_ids
        """
        return self.__online_ids

    @property
    def dists(self) -> list[IPNetAddr]:
        """dists

        Returns:
            list[IPNetAddr]: distinations
        """
        return self.__dists

    def send(self, sim_cmds: SimCommands) -> None:
        """
        送信実行
        :return: None
        """
        # self.__logger.info(sim_cmds)
        send_data = grSim_Commands(
            timestamp=sim_cmds.timestamp,
            isteamyellow=sim_cmds.isteamyellow,
            robot_commands=sim_cmds.to_proto(),
        )

        send_packet = grSim_Packet(commands=send_data)
        packet: bytes = send_packet.SerializeToString()

        for dist in self.dists:
            self.__logger.debug("Sending to %s:%d (%s)", dist.host, dist.port, ("real" if self.is_real else "sim"))
            self.__sock.sendto(packet, (dist.host, dist.port))

    def __stop_robots(self) -> None:
        """stop_robots

        Send stop command to all robots.
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
            self.send(commands)
