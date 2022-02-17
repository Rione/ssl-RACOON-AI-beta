#!/usr/bin/env python3.10
"""offense.py

    This module is for the Offense class.
"""
from turtle import window_width

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget


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
        ui = QPainter(self)
        ui.setPen(QColor(Qt.white))
        ui.setBrush(QColor(Qt.green))
        # print(self.__window_width)
        ui.drawRect(
            int(20 * self.__window_width),
            int(30 * self.__window_height),
            int(520 * self.__window_width),
            int(680 * self.__window_height),
        )
