#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""main.py

    This module is for the Gui class.
"""

import math

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from racoon_ai.networks import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall


class Gui(QWidget, QPainter):
    """Gui
    Args:
        None
    Attributes:
        None
    """

    def __init__(self) -> None:
        super(Gui, self).__init__()
        self.__geometry_width: int = 960
        self.__geometry_height: int = 850
        self.__window_width: float
        self.__window_height: float
        self.__ui: QPainter
        self.__ball: SSL_DetectionBall
        self.__role = QLabel("<h1><i>Role</i></h1>", self)
        self.__at = QLabel("<h3><i>AT</i></h3>", self)
        self.__ai = QLabel("<h3><i>RACOON-AI</i></h3>", self)
        # self.__of0 = QLabel("<h3><i>OF0</i></h3>", self)
        # self.__of1 = QLabel("<h3><i>OF1</i></h3>", self)
        # self.__of2 = QLabel("<h3><i>OF2</i></h3>", self)
        # self.__of3 = QLabel("<h3><i>OF3</i></h3>", self)
        # self.__of4 = QLabel("<h3><i>OF3</i></h3>", self)
        # self.__df0 = QLabel("<h3><i>DF0</i></h3>", self)
        # self.__df1 = QLabel("<h3><i>DF1</i></h3>", self)
        # self.__df2 = QLabel("<h3><i>DF2</i></h3>", self)
        # self.__df3 = QLabel("<h3><i>DF2</i></h3>", self)
        # self.__GK = QLabel("<h3><i>GK</i></h3>", self)

        self._initui()

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__their_robots = vision.yellow_robots
        self.__ball = vision.ball
        self.update()

        # print(self.__ball.x)

    def _initui(self) -> None:
        self.resize(self.__geometry_width, self.__geometry_height)
        self.move(0, 0)
        self.setWindowTitle("RACOON-AI")
        label = QLabel(self)
        # label.setFixedSize(150, 150)
        pixmap = QPixmap("game.jpg")
        label.setPixmap(pixmap.scaledToHeight(32))
        label.move(550, 10)

        self.show()

    def resizeEvent(self, event) -> None:
        """Gui
        Args:
            None
        Attributes:
            None
        """
        coat_width = event.size().width()
        coat_height = event.size().height()
        self.__window_width = coat_width / self.__geometry_width
        self.__window_height = coat_height / self.__geometry_height

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)
        self.__ui.setPen(QColor(Qt.white))

        self.__ui.setBrush(QColor(Qt.gray))
        self._drawRect(20, 30, 520, 680)
        self._drawRect(60, 70, 440, 600)
        self._drawEllipse(280, 370, 30, 30)

        self._drawRect(220, 610, 120, 60)
        self._drawRect(220, 70, 120, 60)

        self._drawRect(250, 669, 60, 10)
        self._drawRect(250, 60, 60, 10)

        self.__ui.setBrush(QColor("orange"))
        self._drawEllipse(int((self.__ball.y * 0.05) + 280), int((self.__ball.x * 0.05) + 370), 2, 2)
        # self.__ui.setBrush(QColor("red"))
        # self._drawEllipse(int((self.__ball.y * 0.05) + 280), int((self.__ball.x * 0.05) + 370), 25, 25)

        self._draw_robots("blue")
        self._draw_robots("yellow")

        self.__ui.setPen(QColor(Qt.black))
        self.__ui.setBrush(QColor(Qt.white))
        self._draw_role()

        # self._drawRect(550, 30, 120, 60)
        self.__ui.end()

    def _draw_role(self) -> None:
        self.__role.move(int(20 * self.__window_width), int(740 * self.__window_height))
        self.__at.move(int(20 * self.__window_width), int(780 * self.__window_height))
        self.__ai.move(10, 5)

    def _draw_robots(self, color: str) -> None:
        if color == "blue":
            self.__ui.setBrush(QColor("blue"))
            robots = self.__our_robots
        else:
            self.__ui.setBrush(QColor("yellow"))
            robots = self.__their_robots

        for robot in robots:
            if robot.x != 0:
                self.__ui.setPen(QColor(Qt.black))
                self.__ui.drawChord(
                    int(((robot.y * 0.05) + 280) * self.__window_width - 6),
                    int(((robot.x * 0.05) + 370) * self.__window_height - 7),
                    14,
                    14,
                    int((math.degrees(robot.orientation) + 320) * 16),
                    280 * 16,
                )
                self.__ui.setPen(QColor(Qt.white))
                self.__ui.drawLine(
                    int(((robot.y * 0.05) + 280) * self.__window_width),
                    int(((robot.x * 0.05) + 370) * self.__window_height),
                    int(
                        (((robot.y * 0.05) + 280) * self.__window_width)
                        - 4 * math.cos(-robot.orientation - math.pi / 2)
                    ),
                    int(
                        (((robot.x * 0.05) + 370) * self.__window_height)
                        - 4 * math.sin(-robot.orientation - math.pi / 2)
                    ),
                )

    def _drawRect(self, val1: int, val2: int, val3: int, val4: int) -> None:
        self.__ui.drawRect(
            int(val1 * self.__window_width),
            int(val2 * self.__window_height),
            int(val3 * self.__window_width),
            int(val4 * self.__window_height),
        )

    def _drawEllipse(self, val1: int, val2: int, val3: int, val4: int) -> None:
        center_circle = QPoint(int(val1 * self.__window_width), int(val2 * self.__window_height))
        self.__ui.drawEllipse(center_circle, val3, val4)
