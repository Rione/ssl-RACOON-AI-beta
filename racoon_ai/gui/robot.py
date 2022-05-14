#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""field.py

    This module is for the Feild class.
"""
import math

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from racoon_ai.observer.observer import Observer


class Robot(QWidget, QPainter):
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer) -> None:
        super(Robot, self).__init__()
        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__ui: QPainter()
        self.__window_width: int = 1
        self.__window_height: int = 1
        self.__observer: Observer = observer

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)
        self.__ui.setBrush(QColor("orange"))
        self._drawEllipse(int((self.__observer.ball.y * 0.05) + 280), int((self.__observer.ball.x * 0.05) + 370), 2, 2)

        self._draw_robots("blue")
        self._draw_robots("yellow")
        self.__ui.end()

    def _draw_robots(self, color: str) -> None:
        if color == "blue":
            self.__ui.setBrush(QColor("blue"))
            robots = self.__observer.our_robots
        else:
            self.__ui.setBrush(QColor("yellow"))
            robots = self.__observer.their_robots

        for robot in robots:
            if robot.x != 0:
                self.__ui.setPen(QColor(Qt.black))
                self.__ui.drawChord(
                    int(((robot.y * 0.05) + 280) * self.__window_width - 6),
                    int(((robot.x * 0.05) + 370) * self.__window_height - 7),
                    14,
                    14,
                    int((math.degrees(robot.theta) + 320) * 16),
                    280 * 16,
                )
                self.__ui.setPen(QColor(Qt.white))
                self.__ui.drawLine(
                    int(((robot.y * 0.05) + 280) * self.__window_width),
                    int(((robot.x * 0.05) + 370) * self.__window_height),
                    int((((robot.y * 0.05) + 280) * self.__window_width) - 4 * math.cos(-robot.theta - math.pi / 2)),
                    int((((robot.x * 0.05) + 370) * self.__window_height) - 4 * math.sin(-robot.theta - math.pi / 2)),
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

    def resizeEvent(self, event) -> None:
        coat_width = event.size().width()
        coat_height = event.size().height()
        self.__window_width = coat_width / self.__geometry_width
        self.__window_height = coat_height / self.__geometry_height
