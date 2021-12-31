#!/usr/bin/env python3.10

"""vision_receiver.py

    This module is for the VisionReceiver class.
"""

import socket
from typing import List

import proto_py.messages_robocup_ssl_detection_pb2
import proto_py.messages_robocup_ssl_geometry_pb2
import proto_py.messages_robocup_ssl_wrapper_pb2
from models.official.vision.detection import (
    DetectionBall,
    DetectionFrame,
    DetectionRobot,
)
from models.official.vision.geometry import (
    GeometryCameraCalibration,
    GeometryData,
    GeometryFieldSize,
)


class VisionReceiver:
    """VisionReceiver

    Args:
        invert (bool): データを反転させるかどうか (default: False)
    """

    def __init__(self, invert: bool = False):

        self.__inverted: bool = invert

        self.__num_of_cameras: int = 4

        self.__packet: str = ""

        self.__data = None

        self.__frames: List[DetectionFrame] = []

        self.__geometries: List[GeometryData] = []

        self.__blue_robots: List[DetectionRobot] = []

        self.__yellow_robots: List[DetectionRobot] = []

        self.__port: int = 10020

        self.__local_address: str = "0.0.0.0"

        self.__multicast_group: str = "224.5.23.2"

        # 受信ソケット作成 (指定ポートへのパケットをすべて受信)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(
            socket.IPPROTO_IP,
            socket.IP_ADD_MEMBERSHIP,
            socket.inet_aton(self.__multicast_group)
            + socket.inet_aton(self.__local_address),
        )
        self.__sock.bind(("", self.__port))

        # コンストラクタでは、Visionを全カメラから受け取るまで待機
        while len(self.__geometries) <= (self.__num_of_cameras - 1):
            self.receive()

    def append_frame(self, frame):
        """
        フレームを追加
        :param frame: DetectionFrameが入ります
        :return: None
        """
        self.__frames.append(frame)

    def append_geometry(self, geometry):
        """
        ジオメトリ情報を追加
        :param geometry: GeometryDataが入ります
        :return: None
        """
        self.__geometries.append(geometry)

    def receive(self):
        """
        受信を行います
        :return: None
        """
        # フレームの初期化
        # TO_DO: geometriesは初期化するか？正直最初だけ受け取れば、参照のみで新規に受け取る必要はないかも
        self.__frames = []
        # ロボット状態の初期化
        self.__yellow_robots = []
        self.__blue_robots = []
        buffer_size: int = 2048
        # データ受け取り開始
        cam_counter: int = 1
        # カメラの台数分ループさせる
        while cam_counter <= self.__num_of_cameras:
            self.__packet, _ = self.__sock.recvfrom(buffer_size)
            self.__data = proto_py.messages_robocup_ssl_wrapper_pb2.SSL_WrapperPacket()
            self.__data.ParseFromString(self.__packet)

            # detectionのフレームを取り出す部分
            if self.__data.HasField("detection"):
                frame = self.get_frame()
                self.append_frame(frame)

            # geometryをデータを取り出す部分
            if self.__data.HasField("geometry"):
                geometry = self.get_geometry()
                self.append_geometry(geometry)

            cam_counter = cam_counter + 1

    def get_frame(self):
        """
        フレーム情報をDetectionFrameの型に置き換えます
        :return: None
        """
        frame_number: int = self.__data.detection.frame_number
        t_sent: float = self.__data.detection.t_sent
        t_capture: float = self.__data.detection.t_capture
        camera_id: int = self.__data.detection.camera_id
        balls: List[DetectionBall] = self.__data.detection.balls
        robots_yellow: List[DetectionRobot] = self.__data.detection.robots_yellow
        robots_blue: List[DetectionRobot] = self.__data.detection.robots_blue

        frame = DetectionFrame(
            frame_number,
            t_sent,
            t_capture,
            camera_id,
            balls,
            robots_yellow,
            robots_blue,
        )
        return frame

    def get_geometry(self):
        """
        ジオメトリ情報をGeometryDataに置き換えます
        :return: None
        """
        field: GeometryFieldSize = self.__data.geometry.field
        calib: GeometryCameraCalibration = self.__data.geometry.calib
        geometry: GeometryData = GeometryData(field, calib, 0)
        return geometry

    def get_balls(self):
        """
        ボール情報をDetectionBallに置き換えます
        :return: None
        """
        balls: List[DetectionBall] = []
        for frame in self.__frames:
            for ball in frame.balls:
                confidence: float = ball.confidence
                area: int = ball.area
                pixel_x: float = ball.pixel_x
                pixel_y: float = ball.pixel_y
                ball_x: float = ball.x
                ball_y: float = ball.y
                ball_z: float = ball.z

                detection_ball: DetectionBall = DetectionBall(
                    confidence, area, pixel_x, pixel_y, ball_x, ball_y, ball_z
                )
                balls.append(detection_ball)

        return balls

    def get_blue_robots(self):
        """
        青ロボットを抽出します
        :return: List[DetectionRobot]
        """
        # 2回目以降の参照は、前の値をそのまま出力
        if len(self.__blue_robots) == 0:
            self.get_robots()

        return self.__blue_robots

    def get_yellow_robots(self):
        """
        黄ロボットを抽出します
        :return: List[DetectionRobot]
        """
        # 2回目以降の参照は、前の値をそのまま出力
        if len(self.__yellow_robots) == 0:
            self.get_robots()

        return self.__yellow_robots

    def get_robots(self):
        """
        全ての色のロボットを抽出します
        :return: List[DetectionRobot]
        """
        blue_robots: List[DetectionRobot] = []
        seen_id_blue: List[int] = []
        yellow_robots: List[DetectionRobot] = []
        seen_id_yellow: List[int] = []
        for frame in self.__frames:
            for robot_b in frame.robots_blue:
                confidence: float = robot_b.confidence
                robot_id: int = robot_b.robot_id
                robot_x: float = robot_b.x
                robot_y: float = robot_b.y
                theta: float = robot_b.orientation
                pixel_x: float = robot_b.pixel_x
                pixel_y: float = robot_b.pixel_y
                height: float = robot_b.height
                detection_robot: DetectionRobot = DetectionRobot(
                    confidence,
                    robot_id,
                    robot_x,
                    robot_y,
                    theta,
                    pixel_x,
                    pixel_y,
                    height,
                )

                if robot_id not in seen_id_blue:
                    seen_id_blue.append(robot_b.robot_id)
                    blue_robots.append(detection_robot)

                # for robot_y in frame.robots_yellow:
                #     confidence: float = robot_y.confidence
                #     robot_id: int = robot_y.robot_id
                #     robot_x: float = robot_y.x
                #     robot_y: float = robot_y.y
                #     theta: float = robot_y.orientation
                #     pixel_x: float = robot_y.pixel_x
                #     pixel_y: float = robot_y.pixel_y
                #     height: float = robot_y.height
                #     detection_robot: DetectionRobot = DetectionRobot(
                #         confidence,
                #         robot_id,
                #         robot_x,
                #         robot_y,
                #         theta,
                #         pixel_x,
                #         pixel_y,
                #         height,
                #     )

                # if robot_id not in seen_id_yellow:
                #     seen_id_yellow.append(robot_y.robot_id)
                #     yellow_robots.append(detection_robot)

        # ロボットを整列(0-10まで)させる
        self.__blue_robots = sorted(blue_robots, key=lambda __x: __x.robot_id)
        self.__yellow_robots = sorted(yellow_robots, key=lambda __x: __x.robot_id)

    def get_fieldsize(self):
        """
        GeometryDataからFieldSizeを抽出します
        :return: List[GeometryFieldSize]
        """
        field_length: int = self.__geometries[0].field.field_length
        field_width: int = self.__geometries[0].field.field_width
        goal_width: int = self.__geometries[0].field.goal_width
        goal_depth: int = self.__geometries[0].field.goal_depth
        boundary_width: int = self.__geometries[0].field.boundary_width
        field_lines = self.__geometries[0].field.field_lines
        field_arcs = self.__geometries[0].field.field_arcs

        # grSimからは出力されなかった(AttributeError).
        # penalty_area_depth = self.__geometries[0].field.penalty_area_depth
        # penalty_area_width = self.__geometries[0].field.penalty_area_width
        penalty_area_depth = 0
        penalty_area_width = 0

        fieldsize: GeometryFieldSize = GeometryFieldSize(
            field_length,
            field_width,
            goal_width,
            goal_depth,
            boundary_width,
            field_lines,
            field_arcs,
            penalty_area_depth,
            penalty_area_width,
        )

        return fieldsize


# 以下、テストコード。コメントアウトして実行すると
# 青チームロボットのロボットIDがそれぞれ出力される。
# test = VisionReceiver()
# blue = test.get_blue_robots()
# for robot in blue:
#     print(robot.robot_id)
