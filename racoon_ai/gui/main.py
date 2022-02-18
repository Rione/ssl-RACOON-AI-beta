#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""main.py

    This module is for the Gui class.
"""

from PyQt5.QtCore import QPoint, Qt  # pylint: disable=no-name-in-module
from PyQt5.QtGui import QColor, QPainter  # pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QWidget  # pylint: disable=no-name-in-module

from racoon_ai.networks import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall


class Gui(QWidget):
    """Gui
    Args:
        None
    Attributes:
        None
    """

    def __init__(self) -> None:
        super(Gui, self).__init__()
        self._initui()
        self.__geometry_width: int = 1300
        self.__geometry_height: int = 850
        self.__window_width: float
        self.__window_height: float
        self.__ui: QPainter
        self.__ball: SSL_DetectionBall
        self.__flag: bool = False

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__flag = True
        self.__our_robots = vision.blue_robots
        self.__ball = vision.ball
        self.update()

        # print(self.__ball.x)

    def _initui(self) -> None:
        self.resize(1300, 850)
        self.move(0, 0)
        self.setWindowTitle("RACOON-AI")
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
        # print(coat_width)
        self.__window_width = coat_width / 1300
        self.__window_height = coat_height / 850

    def paintEvent(self, event) -> None:
        if self.__flag is True:
            self.__ui = QPainter(self)
            self.__ui.setPen(QColor(Qt.white))

            self.__ui.setBrush(QColor(Qt.green))
            self._drawRect(20, 30, 520, 680)
            self._drawRect(60, 70, 440, 600)
            self._drawEllipse(280, 370, 30, 30)

            self._drawRect(220, 610, 120, 60)
            self._drawRect(220, 70, 120, 60)

            self._drawRect(250, 669, 60, 10)
            self._drawRect(250, 60, 60, 10)

            self.__ui.setBrush(QColor("orange"))
            self._drawEllipse(int((self.__ball.y * 0.05) + 280), int((self.__ball.x * 0.05) + 370), 2, 2)

            self.__ui.end()

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
