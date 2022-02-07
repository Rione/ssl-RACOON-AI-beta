#!/usr/bin/env python3.10

"""vision_receiver.py

    This module is for the VisionReceiver class.
"""

import socket
import struct
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

    def __init__(self, port: int = 10006, invert: bool = False) -> None:

        super().__init__(port)

        self.__inverted: bool = invert

        self.__num_of_cameras: int = 4

        self.__ball: Optional[SSL_DetectionBall] = None

        self.__blue_robots: list[SSL_DetectionRobot] = []

        self.__yellow_robots: list[SSL_DetectionRobot] = []

        self.__geometries: Optional[list[SSL_GeometryData]] = None

        self.__field_size: Optional[list[SSL_GeometryFieldSize]] = None

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        mreq = struct.pack("4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        # self.__sock.setsockopt(
        #     socket.IPPROTO_IP,
        #     socket.IP_ADD_MEMBERSHIP,
        #     socket.inet_aton(self.multicast_group) + socket.inet_aton(self.local_address),
        # )
        self.__sock.bind(("", port))

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
        self.__ball = balls[0] if len(balls) else None

        # SSL_DetectionFrameをパースして、SSL_DetectionRobot
        blue_robots = [robot for frame in dframes for robot in frame.robots_blue]
        yellow_robots = [robot for frame in dframes for robot in frame.robots_yellow]

        # ロボットを整列(0-10まで)させる
        self.__blue_robots = sorted(blue_robots, key=lambda __x: __x.robot_id)
        self.__yellow_robots = sorted(yellow_robots, key=lambda __x: __x.robot_id)

        count = -1
        pre_robot_id = -1
        for robot in self.__blue_robots:
            count = count + 1
            if robot.robot_id == pre_robot_id:
                self.__blue_robots.pop(count)
                count = count - 1
            pre_robot_id = robot.robot_id
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
    def ball(self) -> SSL_DetectionBall:
        """balls

        Returns:
            SSL_DetectionBall
        """
        return self.__ball or SSL_DetectionBall()

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
        return self.__blue_robots + self.__yellow_robots
