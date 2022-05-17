#!/usr/bin/env python3.10

"""mw_receiver.py

    This module is for the MwReceiver class.
"""

import socket
from logging import getLogger

from racoon_ai.models.ball import Ball
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.models.robot import Robot
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Goal_Info, RacoonMW_Packet, Referee_Info


class MWReceiver(IPNetAddr):
    """VisionReceiver

    Args:
        host (str): IP or hostname of the server
        port (int): Port number of the vision server
    """

    def __init__(self, host: str = "224.5.23.2", port: int = 10020) -> None:

        super().__init__(host, port)

        self.__logger = getLogger(__name__)

        self.__data: RacoonMW_Packet

        self.__ball: Ball = Ball()

        self.__our_robots: list[Robot] = [Robot(i) for i in range(12)]
        self.__enemy_robots: list[Robot] = [Robot(i) for i in range(12)]

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

        # カメラの台数分ループさせる
        packet: bytes = self.__sock.recv(BUFFSIZE)

        self.__data = RacoonMW_Packet()

        self.__data.ParseFromString(packet)

        self.ball.update(self.__data.ball)

        bot: Robot
        enemy: Robot
        for dbot in self.__data.our_robots:
            if dbot.robot_id < 12:
                bot = self.__our_robots[dbot.robot_id]
                bot.update(dbot)

        for debot in self.__data.enemy_robots:
            if debot.robot_id < 12:
                enemy = self.__enemy_robots[debot.robot_id]
                enemy.update(debot)

    @property
    def ball(self) -> Ball:
        """ball"""
        return self.__ball

    def get_our_robots(self) -> list[Robot]:
        """get_our_robot

        Returns:
            Robot_Infos
        """
        return self.__our_robots

    def get_enemy_robots(self) -> list[Robot]:
        """get_our_robot

        Returns:
            Robot_Infos
        """
        return self.__enemy_robots

    def get_our_robot(self, robot_id: int) -> Robot:
        """get_our_robot

        Returns:
            Robot
        """
        our_robot: Robot
        our_robot = Robot(
            robot_id=99,
        )
        for robot in self.__our_robots:
            if robot_id == robot.robot_id:
                our_robot = robot

        return our_robot

    def get_enemy_robot(self, enemy_id: int) -> Robot:
        """get_enemy_robot

        Returns:
            Enemy
        """
        enemy_robot: Robot
        enemy_robot = Robot(
            robot_id=99,
        )
        for enemy in self.__enemy_robots:
            if enemy_id == enemy.robot_id:
                enemy_robot = enemy

        return enemy_robot

    def get_ball(self) -> Ball:
        """get_ball

        Returns:
            Ball_Info
        """

        return self.__ball

    def get_goal(self) -> Pose:
        """get_goal

        Returns:
            Goal_Info
        """
        goal: Goal_Info = self.__data.goal

        return Pose(goal.x, goal.y)

    def get_referee(self) -> Referee_Info:
        """get_referee

        Returns:
            Referee_Info
        """
        referee: Referee_Info = self.__data.referee

        return referee

    def get_sec_per_frame(self) -> float:
        """get_sec_per_frame

        Returns:
            float
        """
        secperframe: float = self.__data.info.secperframe

        return secperframe

    def get_num_of_cameras(self) -> int:
        """get_num_of_cameras

        Returns:
            int
        """
        numofcameras: int = self.__data.info.num_of_cameras

        return numofcameras

    def is_vision_recv(self) -> bool:
        """is_vision_recv

        Returns:
            bool
        """
        isvisionrecv: bool = self.__data.info.is_vision_recv

        return isvisionrecv

    def get_attack_direction(self) -> int:
        """get_attack_direction

        Returns:
            int
        """
        attackdirection: int = self.__data.info.attack_direction

        return attackdirection
