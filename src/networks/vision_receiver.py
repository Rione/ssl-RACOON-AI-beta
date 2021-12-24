#!/usr/bin/env python3.10
import socket
import proto_py.messages_robocup_ssl_detection_pb2
import proto_py.messages_robocup_ssl_geometry_pb2
import proto_py.messages_robocup_ssl_wrapper_pb2

from models.official.field.detection.detection_ball import DetectionBall
from models.official.field.detection.detection_frame import DetectionFrame
from models.official.field.detection.detection_robot import DetectionRobot
from models.official.field.geometry.geometry_data import GeometryData
from models.official.field.geometry.geometry_field_size import GeometryFieldSize
from models.official.field.geometry.geometry_camera_calibration import (
    GeometryCameraCalibration,
)


class VisionReceiver(object):
    def __init__(self, invert=False):

        self.__inverted = invert

        self.__num_of_cameras = 4

        self.__packet = ""

        self.__data = None

        self.__frames = []

        self.__geometries = []

        self.__blue_robots = []

        self.__yellow_robots = []

        self.__port = 10020

        self.__local_address = "0.0.0.0"

        self.__multicast_group = "224.5.23.2"

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
        self.__frames.append(frame)

    def append_geometry(self, geometry):
        self.__geometries.append(geometry)

    def receive(self):
        # フレームの初期化
        # TODO: geometriesは初期化するか？正直最初だけ受け取れば、参照のみで新規に受け取る必要はないかも
        self.__frames = []
        # ロボット状態の初期化
        self.__yellow_robots = []
        self.__blue_robots = []
        buffer_size = 2048
        # データ受け取り開始
        cam_counter = 1
        # カメラの台数分ループさせる
        while cam_counter <= self.__num_of_cameras:
            self.__packet, recv = self.__sock.recvfrom(buffer_size)
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
        frame_number = self.__data.detection.frame_number
        t_sent = self.__data.detection.t_sent
        t_capture = self.__data.detection.t_capture
        camera_id = self.__data.detection.camera_id
        balls = self.__data.detection.balls
        robots_yellow = self.__data.detection.robots_yellow
        robots_blue = self.__data.detection.robots_blue

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
        field = self.__data.geometry.field
        calib = self.__data.geometry.calib
        geometry = GeometryData(field, calib, 0)
        return geometry

    def get_balls(self):
        balls = []
        for frame in self.__frames:
            for ball in frame.balls:
                confidence = ball.confidence
                area = ball.area
                pixel_x = ball.pixel_x
                pixel_y = ball.pixel_y
                x = ball.x
                y = ball.y
                z = ball.z

                detection_ball = DetectionBall(
                    confidence, area, pixel_x, pixel_y, x, y, z
                )
                balls.append(detection_ball)

        return balls

    def get_blue_robots(self):
        # 2回目以降の参照は、前の値をそのまま出力
        if len(self.__blue_robots) == 0:
            self.get_robots()

        return self.__blue_robots

    def get_yellow_robots(self):
        # 2回目以降の参照は、前の値をそのまま出力
        if len(self.__yellow_robots) == 0:
            self.get_robots()

        return self.__yellow_robots

    def get_robots(self):
        blue_robots = []
        seen_id_blue = []
        yellow_robots = []
        seen_id_yellow = []
        for frame in self.__frames:
            for robot_b in frame.robots_blue:
                confidence = robot_b.confidence
                robot_id = robot_b.robot_id
                x = robot_b.x
                y = robot_b.y
                theta = robot_b.orientation
                pixel_x = robot_b.pixel_x
                pixel_y = robot_b.pixel_y
                height = robot_b.height
                detection_robot = DetectionRobot(
                    confidence, robot_id, x, y, theta, pixel_x, pixel_y, height
                )

                if robot_id not in seen_id_blue:
                    seen_id_blue.append(robot_b.robot_id)
                    blue_robots.append(detection_robot)

            for robot_y in frame.robots_yellow:
                confidence = robot_y.confidence
                robot_id = robot_y.robot_id
                x = robot_y.x
                y = robot_y.y
                theta = robot_y.orientation
                pixel_x = robot_y.pixel_x
                pixel_y = robot_y.pixel_y
                height = robot_y.height
                detection_robot = DetectionRobot(
                    confidence, robot_id, x, y, theta, pixel_x, pixel_y, height
                )

                if robot_id not in seen_id_yellow:
                    seen_id_yellow.append(robot_y.robot_id)
                    yellow_robots.append(detection_robot)

        # ロボットを整列(0-10まで)させる
        self.__blue_robots = sorted(blue_robots, key=lambda __x: __x.robot_id)
        self.__yellow_robots = sorted(yellow_robots, key=lambda __x: __x.robot_id)

    def get_fieldsize(self):
        field_length = self.__geometries[0].field.field_length
        field_width = self.__geometries[0].field.field_width
        goal_width = self.__geometries[0].field.goal_width
        goal_depth = self.__geometries[0].field.goal_depth
        boundary_width = self.__geometries[0].field.boundary_width
        field_lines = self.__geometries[0].field.field_lines
        field_arcs = self.__geometries[0].field.field_arcs

        # grSimからは出力されなかった(AttributeError).
        # penalty_area_depth = self.__geometries[0].field.penalty_area_depth
        # penalty_area_width = self.__geometries[0].field.penalty_area_width
        penalty_area_depth = 0
        penalty_area_width = 0

        fieldsize = GeometryFieldSize(
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
