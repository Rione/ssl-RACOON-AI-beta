#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""main.py

    This module is for the Gui class.
"""

import math
from dataclasses import field

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from racoon_ai import observer
from racoon_ai.gui.field import Field
from racoon_ai.gui.robot import Robot  # type: ignore
from racoon_ai.observer.observer import Observer
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall


class Gui(QWidget, QPainter):
    """Gui
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: Observer) -> None:
        super(Gui, self).__init__()
        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__window_width: float = 1.0
        self.__window_height: float = 1.0
        self.__observer = observer
        self.__robot = Robot(observer)
        self.__field = Field(observer)
        self._initui()

    def active(self) -> None:
        self.update()

    def _initui(self) -> None:
        self.__role = QLabel("<h1><i>Role</i></h1>", self)
        self.__at = QLabel("<h3><i>AT</i></h3>", self)
        self.__ai = QLabel("<h3><i>RACOON-AI</i></h3>", self)
        self.resize(self.__geometry_width, self.__geometry_height)
        self.move(0, 0)
        self.setWindowTitle("RACOON-AI")
        label = QLabel(self)
        pixmap = QPixmap("barger.png")
        label.setPixmap(pixmap.scaledToHeight(32))
        label.move(800, 10)

        self.__grid = QGridLayout()
        self.__grid.addWidget(self.__field, 0, 0)
        self.__grid.addWidget(self.__robot, 0, 0)

        self.setLayout(self.__grid)

        self.show()

    def resizeEvent(self, event) -> None:
        coat_width = event.size().width()
        coat_height = event.size().height()
        self.__window_width = coat_width / self.__geometry_width
        self.__window_height = coat_height / self.__geometry_height

    def _draw_role(self) -> None:
        self.__role.move(int(20 * self.__window_width), int(740 * self.__window_height))
        self.__at.move(int(20 * self.__window_width), int(780 * self.__window_height))
        self.__ai.move(10, 5)
