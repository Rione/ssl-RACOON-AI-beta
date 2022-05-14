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
        self.__observer: Observer = observer

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.setBrush(QColor(Qt.gray))

        # Feild全体
        self._drawRect(20, 30, 520, 680)
        # Feild line
        self._drawRect(60, 70, 440, 600)
        # Center line
        self._drawEllipse(280, 370, 30, 30)
        # Down Goal line
        self._drawRect(220, 610, 120, 60)
        # Up Goal line
        self._drawRect(220, 70, 120, 60)
        # Down Goal
        self._drawRect(250, 669, 60, 10)
        # Up Goal
        self._drawRect(250, 60, 60, 10)

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
