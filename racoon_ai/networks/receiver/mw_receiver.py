#!/usr/bin/env python3.10

"""mw_receiver.py

    This module is for the MwReceiver class.
"""

from logging import getLogger
from socket import AF_INET, IPPROTO_UDP, SO_REUSEADDR, SOCK_DGRAM, SOL_SOCKET, socket
from typing import Optional

from racoon_ai.models.ball import Ball
from racoon_ai.models.coordinate import Point
from racoon_ai.models.geometry import Geometry
from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.models.referee import Referee
from racoon_ai.models.robot import Robot
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import RacoonMW_Packet, Robot_Infos


class MWReceiver(IPNetAddr):
    """VisionReceiver

    Args:
        target_ids (list[int]): Target robot IDs
        is_team_yellow (bool, optional): If true, the team is yellow (default: False)
        host (str): IP or hostname of the server
        port (int): Port number of the vision server
    """

    def __init__(
        self,
        target_ids: list[int],
        is_team_yellow: bool = False,
        *,
        host: str = "127.0.0.1",
        port: int = 30011,
    ) -> None:

        super().__init__(host, port)

        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")

        self.__ball: Ball = Ball()
        self.__geometry: Geometry = Geometry()
        self.__referee: Referee = Referee()

        self.__target_ids: list[int] = target_ids
        self.__is_team_yellow: bool = is_team_yellow

        self.__our_robots: list[Robot] = [Robot(i) for i in range(12)]
        self.__enemy_robots: list[Robot] = [Robot(i) for i in range(12)]

        self.__sec_per_frame: float
        self.__n_camras: int
        self.__num_of_our_robots: int
        self.__num_of_enemy_robots: int
        self.__is_vision_recv: bool
        self.__attack_direction: int

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))

        self.main()

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__sock.close()
        self.__logger.info("Socket closed")

    def main(self) -> None:
        """main"""
        # Receive data from RACOON-MW
        packet: bytes = self.__sock.recv(BUFFSIZE)
        proto = RacoonMW_Packet()
        proto.ParseFromString(packet)
        self.__logger.debug("Received %s", proto)
        self.update(proto)

    def update(self, proto: RacoonMW_Packet) -> None:
        """update

        Args:
            proto (RacoonMW_Packet): Parsed packet
        """
        self.ball.update(proto.ball)
        self.__logger.debug("Ball: %s", self.ball)

        self.geometry.update(proto.geometry)
        self.__logger.debug("Geometry: %s", self.geometry)

        self.referee.update(proto.referee)
        self.__logger.debug("Referee: %s", self.referee)

        bot: Optional[Robot]
        proto_bot: Robot_Infos
        for proto_bot in proto.our_robots:
            bot = self.get_our_by_id(proto_bot.robot_id, False, False)
            if bot is not None:
                bot.update(proto_bot)
                self.__logger.debug(bot)
            else:
                self.__logger.warning("Our robot %d could not be set", proto_bot.robot_id)

        for proto_bot in proto.enemy_robots:
            bot = self.get_enemy_by_id(proto_bot.robot_id, False, False)
            if bot is not None:
                bot.update(proto_bot)
                self.__logger.debug(bot)
            else:
                self.__logger.warning("Enemy robot %d could not be set", proto_bot.robot_id)

        self.__sec_per_frame = proto.info.secperframe

        self.__n_camras = proto.info.num_of_cameras

        self.__num_of_our_robots = proto.info.num_of_our_robots

        self.__num_of_enemy_robots = proto.info.num_of_enemy_robots

        self.__is_vision_recv = proto.info.is_vision_recv

        self.__attack_direction = proto.info.attack_direction

    @property
    def ball(self) -> Ball:
        """ball

        Returns:
            Ball
        """
        return self.__ball

    @property
    def geometry(self) -> Geometry:
        """geometry

        Returns:
            Geometry
        """
        return self.__geometry

    @property
    def referee(self) -> Referee:
        """referee

        Returns:
            Referee
        """
        return self.__referee

    @property
    def our_robots(self) -> list[Robot]:
        """our_robot

        Returns:
            list[Robot]
        """
        return self.__our_robots

    @property
    def enemy_robots(self) -> list[Robot]:
        """enemy_robots

        Returns:
            list[Robot]
        """
        return self.__enemy_robots

    def get_our_by_id(self, robot_id: int, only_online: bool = False, only_visible: bool = True) -> Optional[Robot]:
        """get_our_by_id

        Args:
            robot_id (int): Robot ID
            only_online (bool, optional): If true, only return online robot (default: False)
            only_visible (bool, optional): If true, only return visible robot (default: True)

        Returns:
            Optional[Robot]: None if not found
        """
        return self.__binary_search(
            robot_id,
            maximum=len(self.__our_robots),
            only_online=only_online,
            only_visible=only_visible,
        )

    def get_enemy_by_id(self, enemy_id: int, only_online: bool = False, only_visible: bool = True) -> Optional[Robot]:
        """get_enemy_by_id

        Args:
            enemy_id (int): Enemy ID
            only_online (bool, optional): If true, only return online robot (default: False)
            only_visible (bool, optional): If true, only return visible robot (default: True)

        Returns:
            Optional[Robot]: None if not found
        """
        return self.__binary_search(
            enemy_id,
            maximum=len(self.__enemy_robots),
            search_enemy=True,
            only_online=only_online,
            only_visible=only_visible,
        )

    def __binary_search(
        self,
        target_id: int,
        minimum: int = 0,
        maximum: int = 12,
        search_enemy: bool = False,
        only_online: bool = False,
        only_visible: bool = True,
    ) -> Optional[Robot]:
        """__binary_search

        Args:
            target_id (int): Target robot id
            minimum (int): Minimum index of the list (default: 0)
            maximum (int): Maximum index (default: 12)
            search_enemy (bool, optional): If true, search enemy (default: False)
            only_online (bool, optional): If True, only online robots are returned (default: False)
            only_visible (bool, optional): If True, only visible robots are returned (default: True)

        Returns:
            Optional[Robot]
        """
        self.__logger.debug(
            "Search robot (only_online: %s, only_visible: %s, search_enemy: %s): target=%d, min=%d, max=%d",
            only_online,
            only_visible,
            search_enemy,
            target_id,
            minimum,
            maximum,
        )

        if maximum < minimum:
            return None

        bots: list[Robot] = self.our_robots if (not search_enemy) else self.enemy_robots
        mid = (minimum + maximum) // 2

        if mid == target_id:
            # NOTE: Equivalent to `(not search_enemy) and (not (mid in self.__target_ids))`
            if not ((search_enemy) or (target_id in self.__target_ids)):
                a = 0
                #self.__logger.warning("Robot %d is not in our target ids", target_id)

            bot: Robot = bots[mid]
            if only_online and (not bot.is_online):
                #self.__logger.warning("Robot id %d is invalid", mid)
                a = 0
                return None
            if only_visible and (not bot.is_visible):
                a = 0
                #self.__logger.warning("Robot id %d is not on stage", mid)
                return None

            self.__logger.debug("Bot: %s", bot)
            return bot

        if mid < target_id:
            return self.__binary_search(target_id, (mid + 1), maximum, search_enemy, only_online, only_visible)
        return self.__binary_search(target_id, minimum, (mid - 1), search_enemy, only_online, only_visible)

    @property
    def goal(self) -> Point:
        """goal

        Give goal point

        Returns:
            Point
        """
        return Point(self.__geometry.goal_x, self.__geometry.goal_y)

    @property
    def sec_per_frame(self) -> float:
        """sec_per_frame

        Seconds Per Frame
        NOT FPS

        Returns:
            float
        """
        return self.__sec_per_frame

    @property
    def num_of_cameras(self) -> int:
        """num_of_cameras

        How many cameras used

        Returns:
            int
        """
        return self.__n_camras

    @property
    def num_of_our_robots(self) -> int:
        """num_of_our_robots

        How many our robots visible

        Returns:
            int
        """
        return self.__num_of_our_robots

    @property
    def num_of_enemy_robots(self) -> int:
        """num_of_enemy_robots

        How many enemy robots visible

        Returns:
            int
        """
        return self.__num_of_enemy_robots

    @property
    def num_of_all_robots(self) -> int:
        """num_of_all_robots

        How many all robots visible

        Returns:
            int
        """
        return self.__num_of_enemy_robots + self.__num_of_our_robots

    @property
    def is_vision_recv(self) -> bool:
        """is_vision_recv

        Returns:
            bool
        """
        return self.__is_vision_recv

    @property
    def is_team_yellow(self) -> bool:
        """is_team_yellow

        Returns:
            bool
        """
        return self.__is_team_yellow

    @property
    def attack_direction(self) -> int:
        """attack_direction

        Returns:
            int
        """
        return self.__attack_direction
