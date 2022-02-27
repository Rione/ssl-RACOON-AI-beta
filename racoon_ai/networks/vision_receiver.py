#!/usr/bin/env python3.10

"""vision_receiver.py

    This module is for the VisionReceiver class.
"""

import socket
from logging import getLogger
from operator import attrgetter
from struct import pack

from racoon_ai.models.network import BUFFSIZE, IPNetAddr
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionFrame, SSL_DetectionRobot
from racoon_ai.proto.pb_gen.ssl_vision_geometry_pb2 import SSL_GeometryData, SSL_GeometryFieldSize
from racoon_ai.proto.pb_gen.ssl_vision_wrapper_pb2 import SSL_WrapperPacket


class VisionReceiver(IPNetAddr):
    """VisionReceiver

    Args:
        host (str): IP or hostname of the server
        port (int): Port number of the vision server
    """

    def __init__(self, host: str = "224.5.23.2", port: int = 10020) -> None:

        super().__init__(host, port)

        self.__logger = getLogger(__name__)

        self.__num_of_cameras: int = 4

        self.__balls: list[SSL_DetectionBall] = []

        self.__blue_robots: list[SSL_DetectionRobot] = []

        self.__yellow_robots: list[SSL_DetectionRobot] = []

        self.__geometries: list[SSL_GeometryData] = []

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.host, self.port))

        # マルチキャストグループに接続
        # NOTE: INADDR_ANYは、すべてのIFで受信する
        mreq: bytes = pack("4sL", socket.inet_aton(self.host), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # コンストラクタでは、Visionを全カメラから受け取るまで待機
        while len(self.__geometries) <= (self.__num_of_cameras - 1):
            self.recv()

    def __del__(self) -> None:
        self.__logger.debug("Destructor called")
        self.__sock.close()
        self.__logger.info("Socket closed")

    def recv(self) -> None:
        """recv

        Recieve a packet from the vision server.
        """

        # カメラの台数分ループさせる
        packets: list[bytes] = [self.__sock.recv(BUFFSIZE) for _ in range(self.__num_of_cameras)]

        # パケットをパースして、SSL_WrapperPacketに格納
        wrappers: list[SSL_WrapperPacket] = [SSL_WrapperPacket() for _ in range(self.__num_of_cameras)]
        _: list[int] = [wrappers[i].ParseFromString(packet) for i, packet in enumerate(packets)]

        # パケットをパースして、list[SSL_GeometryData]に格納
        self.__geometries = [wrapper.geometry for wrapper in wrappers if wrapper.HasField("geometry")]

        # パケットをパースして、list[SSL_DetectionFrame]に格納
        dframes: list[SSL_DetectionFrame] = [
            wrapper.detection for i, wrapper in enumerate(wrappers) if wrappers[i].HasField("detection")
        ]

        # SSL_DetectionFrameをパースして、SSL_DetectionBall
        balls: list[SSL_DetectionBall] = [ball for frame in dframes for ball in frame.balls]
        self.__balls = sorted(balls, key=attrgetter("confidence"), reverse=True) if balls else []

        # SSL_DetectionFrameをパースして、SSL_DetectionRobot
        blue_robots = [robot for frame in dframes for robot in frame.robots_blue]
        yellow_robots = [robot for frame in dframes for robot in frame.robots_yellow]

        # ロボットを整列(0-10まで)させる
        self.__blue_robots = sorted(blue_robots, key=attrgetter("robot_id")) if blue_robots else []
        self.__yellow_robots = sorted(yellow_robots, key=attrgetter("robot_id")) if yellow_robots else []

    @property
    def num_of_cameras(self) -> int:
        """num_of_cameras

        Return:
            int: カメラの台数
        """
        return self.__num_of_cameras

    @property
    def balls(self) -> list[SSL_DetectionBall]:
        """balls

        Returns:
            List[SSL_DetectionBall]
        """
        return self.__balls

    @property
    def blue_robots(self) -> list[SSL_DetectionRobot]:
        """blue_robots
        青ロボットを抽出します

        Return:
            List[DetectionRobot]
        """
        return self.__blue_robots

    @property
    def yellow_robots(self) -> list[SSL_DetectionRobot]:
        """yellow_robots
        黄ロボットを抽出します

        Return:
            List[DetectionRobot]
        """
        return self.__yellow_robots

    @property
    def all_robots(self) -> list[SSL_DetectionRobot]:
        """get_all_robots

        Returns:
            List[SSL_DetectionRobot]
        """
        return self.blue_robots + self.yellow_robots

    @property
    def field_size(self) -> list[SSL_GeometryFieldSize]:
        """field_size

        Returns:
            List[SSL_GeometryFieldSize]
        """
        return [geometry.field for geometry in self.__geometries]
