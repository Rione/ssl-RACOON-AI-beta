#!/usr/bin/env python3.10

"""vision_receiver.py

    This module is for the VisionReceiver class.
"""

import socket
from operator import attrgetter
from struct import pack
from typing import Optional

from racoon_ai.models.network import BUFFSIZE, Network
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionFrame, SSL_DetectionRobot
from racoon_ai.proto.pb_gen.ssl_vision_geometry_pb2 import SSL_GeometryData, SSL_GeometryFieldSize
from racoon_ai.proto.pb_gen.ssl_vision_wrapper_pb2 import SSL_WrapperPacket


class VisionReceiver(Network):
    """VisionReceiver

    Args:
        invert (bool): データを反転させるかどうか (default: False)
    """

    def __init__(self, port: int = 10020, invert: bool = False) -> None:

        super().__init__(port)

        self.__inverted: bool = invert

        self.__num_of_cameras: int = 4

        self.__balls: list[SSL_DetectionBall] = []

        self.__blue_robots: list[SSL_DetectionRobot] = []

        self.__yellow_robots: list[SSL_DetectionRobot] = []

        self.__geometries: Optional[list[SSL_GeometryData]] = None

        self.__field_size: Optional[list[SSL_GeometryFieldSize]] = None

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind((self.multicast_group, self.port))

        # マルチキャストグループに接続
        # NOTE: INADDR_ANYは、すべてのIFで受信する
        mreq: bytes = pack("4sL", socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # コンストラクタでは、Visionを全カメラから受け取るまで待機
        while self.__geometries is None or len(self.__geometries) <= (self.__num_of_cameras - 1):
            self.receive()

    def __del__(self) -> None:
        self.__sock.close()

    def receive(self) -> None:
        """recieve

        受信を行います

        Return:
            None
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

        # フィールドサイズを取得
        self.__field_size = [geometry.field for geometry in self.__geometries]

    @property
    def inverted(self) -> bool:
        """inverted

        Return:
            bool: データを反転させるかどうか
        """
        return self.__inverted

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

        Note:
            2回目以降の参照は、前の値をそのまま出力
        """
        return self.__blue_robots

    @property
    def yellow_robots(self) -> list[SSL_DetectionRobot]:
        """yellow_robots
        黄ロボットを抽出します

        Return:
            List[DetectionRobot]

        Note:
            2回目以降の参照は、前の値をそのまま出力
        """
        return self.__yellow_robots

    @property
    def field_size(self) -> Optional[list[SSL_GeometryFieldSize]]:
        """field_size

        Returns:
            List[SSL_GeometryFieldSize] | None
        """
        return self.__field_size

    def get_all_robots(self) -> list[SSL_DetectionRobot]:
        """get_all_robots

        Returns:
            List[SSL_DetectionRobot]
        """
        return self.blue_robots + self.yellow_robots

    def get_ball(self) -> SSL_DetectionBall:
        """balls

        Returns:
            SSL_DetectionBall
        """
        return self.balls[0] if self.balls else SSL_DetectionBall()
