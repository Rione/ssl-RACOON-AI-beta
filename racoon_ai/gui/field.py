#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""field.py

    This module is for the Feild class.
"""
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget

from racoon_ai.networks.receiver import MWReceiver


class Field(QWidget, QPainter):
    """Field
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer) -> None:
        super(Field, self).__init__()
        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__ui: QPainter()
        self.__window_width: float = 1.0
        self.__window_height: float = 1.0
        self.__observer: MWReceiver = observer

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)

        self.__ui.setPen(QColor(Qt.white))
        self.__ui.setBrush(QColor(Qt.gray))

        # Feild全体
        self.__ui.drawRect(25, 20, 520, 730)
        # Feild line
        self.__ui.drawRect(65, 60, 440, 650)
        # Center line
        self.__ui.drawEllipse(260, 340, 30, 30)
        # Down Goal line
        self.__ui.drawRect(220, 650, 120, 60)
        # Up Goal line
        self.__ui.drawRect(220, 60, 120, 60)
        # Down Goal
        self.__ui.drawRect(250, 709, 60, 10)
        # Up Goal
        self.__ui.drawRect(250, 50, 60, 10)

        self.__ui.setPen(QColor(Qt.black))
        self.__ui.setBrush(QColor(Qt.white))

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

    def resizeEvent(self, event) -> None:
        coat_width = event.size().width()
        coat_height = event.size().height()
        self.__window_width = coat_width / self.__geometry_width
        self.__window_height = coat_height / self.__geometry_height
