#!/usr/bin/env python3.10

"""command_sender.py

    This module is for the CommandSender class.
"""

from logging import Logger, getLogger
from socket import AF_INET, IP_MULTICAST_TTL, IPPROTO_IP, IPPROTO_UDP, SOCK_DGRAM, socket
from time import perf_counter, sleep

from racoon_ai.models.network import IPNetAddr
from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.proto.pb_gen.grSim_Commands_pb2 import grSim_Commands
from racoon_ai.proto.pb_gen.grSim_Packet_pb2 import grSim_Packet


class CommandSender:
    """CommandSender

    Args:
        target_ids (set[int]): Target robot IDs.
        is_real (bool, optional): True if this is a real robot. Defaults to False.
        is_team_yellow (bool, optional): True if this is our team is yellow. Defaults to False.
        host (str, optional): IP address of the target.
            Defaults to `224.5.23.2`.
        port (int, optional): Port number of the target.
            Defaults to `20011`.

    TODO:
        Implement a method to change the address and port on the fly.
    """

    def __init__(
        self,
        target_ids: set[int],
        is_real: bool = False,
        is_team_yellow: bool = False,
        *,
        host: str = "224.5.23.2",
        port: int = 20011,
    ) -> None:

        self.__logger: Logger = getLogger(__name__)

        self.__is_real: bool = is_real

        self.__is_team_yellow: bool = is_team_yellow

        self.__target_ids: set[int] = target_ids

        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

        self.__dists: set[IPNetAddr]

        if self.__is_real and self.__target_ids:
            host_ips: set[str] = {f"192.168.0.1{robot_id:02d}" for robot_id in self.__target_ids}
            self.__dists = {IPNetAddr(host, port, mod_name=__name__) for host in host_ips}
            self.__imu_reset()
            sleep(0.1)
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
                ("real" if self.__is_real else "sim"),
            )
            self.__sock.sendto(packet, (dist.host, dist.port))

    def __imu_reset(self, count: int = 10) -> None:
        """reset_imu

        Send reset IMU command to all robots.
        """
        self.__logger.info("Resetting IMU...")
        commands: SimCommands = SimCommands(
            isteamyellow=self.__is_team_yellow,
            robot_commands=[RobotCommand(254)],
        )

        start: float = perf_counter()
        for _ in range(count):
            self.send(commands)
        self.__logger.info("Sent reset IMU for %.3f seconds", perf_counter() - start)

    def __stop_robots(self, count: int = int(1e4)) -> None:
        """stop_robots

        Send stop command to all robots.
        """
        self.__logger.info("Stopping robots...")

        id_set: set[int] = {255} if self.__is_real else self.__target_ids
        self.__logger.info("Robot IDs: %s", id_set)

        commands: SimCommands = SimCommands(
            isteamyellow=self.__is_team_yellow,
            robot_commands=[RobotCommand(i) for i in id_set],
        )

        start: float = perf_counter()
        for _ in range(count):
            self.send(commands)
        self.__logger.info("Sent stop for %.3f seconds", perf_counter() - start)
