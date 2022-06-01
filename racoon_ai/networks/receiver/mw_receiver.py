#!/usr/bin/env python3.10

"""mw_receiver.py

    This module is for the MwReceiver class.
"""

import socket
from logging import getLogger
from typing import Optional

from racoon_ai.models.ball import Ball
from racoon_ai.models.coordinate import Point
from racoon_ai.models.geometry import Geometry
from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.models.referee import Referee
from racoon_ai.models.robot import Robot
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Geometry_Info, RacoonMW_Packet


class MWReceiver(IPNetAddr):
    """VisionReceiver

    Args:
        host (str): IP or hostname of the server
        port (int): Port number of the vision server
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 30011) -> None:

        super().__init__(host, port)

        self.__logger = getLogger(__name__)

        self.__data: RacoonMW_Packet

        self.__ball: Ball = Ball()
        self.__geometry: Geometry = Geometry()
        self.__referee: Referee = Referee()
        self.__our_robots: list[Robot] = [Robot(i) for i in range(11)]
        self.__enemy_robots: list[Robot] = [Robot(i) for i in range(11)]

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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

        self.__data = RacoonMW_Packet()

        self.__data.ParseFromString(packet)

        self.ball.update(self.__data.ball)

        self.geometry.update(self.__data.geometry)

        self.referee.update(self.__data.referee)

        bot: Robot
        enemy: Robot
        for dbot in self.__data.our_robots:
            if dbot.robot_id < 11:
                bot = self.__our_robots[dbot.robot_id]
                bot.update(dbot)

        for debot in self.__data.enemy_robots:
            if debot.robot_id < 11:
                enemy = self.__enemy_robots[debot.robot_id]
                enemy.update(debot)

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

    def get_our_by_id(self, robot_id: int) -> Optional[Robot]:
        """get_our_by_id

        Returns:
            Optional[Robot]
        """
        for robot in self.__our_robots:
            if robot_id == robot.robot_id:
                return robot
        return None

    def get_enemy_by_id(self, enemy_id: int) -> Optional[Robot]:
        """get_enemy_by_id

        Returns:
            Robot
        """
        for enemy in self.__enemy_robots:
            if enemy_id == enemy.robot_id:
                return enemy
        return None

    @property
    def goal(self) -> Point:
        """goal

        Give goal point

        Returns:
            Point
        """
        goal: Geometry_Info = self.__data.geometry

        return Point(goal.goal_x, goal.goal_y)

    @property
    def sec_per_frame(self) -> float:
        """sec_per_frame

        Seconds Per Frame
        NOT FPS

        Returns:
            float
        """
        secperframe: float = self.__data.info.secperframe

        return secperframe

    @property
    def num_of_cameras(self) -> int:
        """num_of_cameras

        How many cameras used

        Returns:
            int
        """
        numofcameras: int = self.__data.info.num_of_cameras

        return numofcameras

    @property
    def is_vision_recv(self) -> bool:
        """is_vision_recv

        Returns:
            bool
        """
        isvisionrecv: bool = self.__data.info.is_vision_recv

        return isvisionrecv

    @property
    def attack_direction(self) -> int:
        """attack_direction

        Returns:
            int
        """
        attackdirection: int = self.__data.info.attack_direction

        return attackdirection
