#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

from logging import getLogger
from socket import AF_INET, IP_MULTICAST_TTL, IPPROTO_IP, IPPROTO_UDP, SOCK_DGRAM, socket

from racoon_ai.models.network import IPNetAddr
from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.observer import Observer
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Commands
from racoon_ai.proto.pb_gen.grSim_Packet_pb2 import grSim_Packet


class CommandSender:
    """CommandSender

    Args:
        observer (Observer): Observer instance.
        host (str, optional): IP address of the target.
            Defaults to `224.5.23.2`.
        port (int, optional): Port number of the target.
            Defaults to `20011`.

    TODO:
        Implement a method to change the address and port on the fly.
    """

    def __init__(
        self,
        observer: Observer,
        *,
        host: str = "224.5.23.2",
        port: int = 20011,
    ) -> None:

        self.__logger = getLogger(__name__)

        self.__observer: Observer = observer

        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

        self.__dists: set[IPNetAddr]

        if self.__observer.is_real and self.__observer.target_ids:
            host_ips: set[str] = {f"192.168.100.1{robot_id:02d}" for robot_id in self.__observer.target_ids}
            self.__dists = {IPNetAddr(host, port, mod_name=__name__) for host in host_ips}
            return

        self.__dists = {IPNetAddr(host, port, mod_name=__name__)}
        self.__sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__stop_robots()
        self.__sock.close()
        self.__logger.info("Socket closed")

    @property
    def dists(self) -> set[IPNetAddr]:
        """dists

        Returns:
            set[IPNetAddr]: distinations
        """
        return self.__dists

    def send(self, sim_cmds: SimCommands) -> None:
        """
        送信実行
        :return: None
        """
        send_data = grSim_Commands(
            timestamp=sim_cmds.timestamp,
            isteamyellow=sim_cmds.isteamyellow,
            robot_commands=sim_cmds.to_proto(),
        )

        send_packet = grSim_Packet(commands=send_data)
        self.__logger.debug("Sending packet %s", send_packet)

        packet: bytes = send_packet.SerializeToString()
        self.__logger.debug("Sending packet: %s", packet)

        for dist in set(self.dists):
            self.__logger.debug(
                "Sending to %s:%d (%s)",
                dist.host,
                dist.port,
                ("real" if self.__observer.is_real else "sim"),
            )
            self.__sock.sendto(packet, (dist.host, dist.port))

    def __stop_robots(self, count: int = int(1e4)) -> None:
        """stop_robots

        Send stop command to all robots.
        """
        self.__logger.info("Stopping robots...")
        commands: SimCommands = SimCommands(
            isteamyellow=self.__observer.is_team_yellow,
            robot_commands=[
                RobotCommand(i)
                for i in set(
                    self.__observer.target_ids
                    or (
                        bot.robot_id
                        for bot in set(
                            self.__observer.get_our_by_id(bid)
                            for bid in range(self.__observer.num_of_our_vision_robots)
                        )
                        if bot
                    )
                )
            ],
        )
        for _ in range(count):
            self.send(commands)
