#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""background.py

    This module is for the Back class.
"""

from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from racoon_ai.observer.observer import Observer


class Back(QWidget, QPainter):
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer) -> None:
        super(Back, self).__init__()
        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__ui: QPainter()
        self.__window_width: float = 1.0
        self.__window_height: float = 1.0
        self.__observer: Observer = observer

        self._set_text()
        self._set_image()

    def _set_text(self) -> None:
        self.__ai_text = QLabel("RACOON-AI", self)
        self.__ai_text.setGeometry(0, 0, 150, 50)
        self.__ai_text.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__ai_text.setStyleSheet("background-color: white")
        self.__ai_text.setStyleSheet("QLabel { color : white; }")
        self.__ai_text.move(50, -5)

    def _set_image(self) -> None:
        self.__pixmap_racoon = QPixmap("images/racoon2.png")
        self.__pixmap_game = QPixmap("images/game_2.png")
        self.__pixmap_block = QPixmap("images/block.png")
        self.__pixmap_referee = QPixmap("images/referee.png")
        self.__pixmap_gear = QPixmap("images/gear.png")

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)

        self.__ui.setBrush(QColor("#2E333A"))  # 背景
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawRect(0, 0, 3000, 1000)

        self.__ui.setBrush(QColor("#1E1E1E"))  # 上部
        self.__ui.setPen(QColor("#1E1E1E"))
        self.__ui.drawRect(0, 0, 3000, 40)

        self.__ui.setBrush(QColor("#1E1E1E"))  # サイドバー
        self.__ui.setPen(QColor("#1E1E1E"))
        self.__ui.drawRect(0, 90, 45, 1000)

        self.__ui.setPen(QColor("white"))  # ハイライト
        self.__ui.drawLine(1, 42, 1, 88)

        self.__ui.drawPixmap(8, 7, 30, 25, self.__pixmap_racoon)
        self.__ui.drawPixmap(6, 50, 34, 32, self.__pixmap_block)
        self.__ui.drawPixmap(4, 100, 35, 38, self.__pixmap_game)
        self.__ui.drawPixmap(0, 145, 42, 40, self.__pixmap_referee)
        self.__ui.drawPixmap(-2, 193, 44, 45, self.__pixmap_gear)

        self.__ui.end()

    def resizeEvent(self, event) -> None:
        coat_width = event.size().width()
        coat_height = event.size().height()
        self.__window_width = coat_width / self.__geometry_width
        self.__window_height = coat_height / self.__geometry_height
