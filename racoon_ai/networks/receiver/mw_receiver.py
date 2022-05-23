#!/usr/bin/env python3.10

"""mw_receiver.py

    This module is for the MwReceiver class.
"""

import socket
from logging import getLogger

from racoon_ai.models.ball import Ball
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.geometry import Geometry
from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.models.robot import Robot
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Geometry_Info, RacoonMW_Packet, Referee_Info


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
        self.__geometry: Geometry = Geometry()
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

        self.geometry.update(self.__data.geometry)

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

        print(self.geometry)

    @property
    def ball(self) -> Ball:
        """ball"""
        return self.__ball

    @property
    def geometry(self) -> Geometry:
        """geometry"""
        return self.__geometry

    @property
    def our_robots(self) -> list[Robot]:
        """get_our_robot

        Returns:
            Robot_Infos
        """
        return self.__our_robots

    @property
    def enemy_robots(self) -> list[Robot]:
        """get_our_robot

        Returns:
            Robot_Infos
        """
        return self.__enemy_robots

    def get_our_by_id(self, robot_id: int) -> Robot:
        """get_our_by_id

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

    def get_enemy_by_id(self, enemy_id: int) -> Robot:
        """get_enemy_by_id

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

    @property
    def goal(self) -> Pose:
        """goal

        Returns:
            Goal_Info
        """
        goal: Geometry_Info = self.__data.geometry

        return Pose(goal.goal_x, goal.goal_y)

    @property
    def ref_command_int(self) -> int:
        """referee

        Returns:
            Referee_Info
        """
        referee: Referee_Info = self.__data.referee

        return int(referee.command)

    @property
    def ref_pre_command(self) -> int:
        """referee

        Returns:
            Referee_Info
        """
        referee: Referee_Info = self.__data.referee

        return int(referee.pre_command)

    @property
    def ref_red_cards(self) -> int:
        """referee

        Returns:
            Referee_Info
        """
        referee: Referee_Info = self.__data.referee

        return int(referee.red_cards)

    @property
    def ref_yellow_cards(self) -> int:
        """referee

        Returns:
            Referee_Info
        """
        referee: Referee_Info = self.__data.referee

        return int(referee.yellow_cards)

    @staticmethod
    def get_ref_command_str_by_int(command_id: int) -> str:
        """referee

        Returns:
            Referee_Info
        """
        commands: list[str] = Referee_Info.Command.keys()
        return commands[command_id]

    @property
    def ref_command_str(self) -> str:
        """referee

        Returns:
            Referee_Info
        """

        referee: Referee_Info = self.__data.referee

        commands: list[str] = Referee_Info.Command.keys()
        return commands[referee.command]

    @property
    def sec_per_frame(self) -> float:
        """sec_per_framed

        Returns:
            float
        """
        secperframe: float = self.__data.info.secperframe

        return secperframe

    @property
    def num_of_cameras(self) -> int:
        """num_of_cameras

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
