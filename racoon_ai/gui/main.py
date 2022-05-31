#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""main.py

    This module is for the Gui class.
"""

import math
from dataclasses import field
from random import randint
from re import X

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
from PyQt5.QtChart import QChart, QChartView, QDateTimeAxis, QLineSeries, QValueAxis
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget
from pyqtgraph import PlotWidget, plot

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
        self.__ui: QPainter
        self.__geometry_width: int = 590
        self.__geometry_height: int = 850
        self.__robot = Robot(observer)
        self.__field = Field(observer)
        self._initui()

    def _initui(self) -> None:
        self.resize(self.__geometry_width, self.__geometry_height)
        self.setWindowTitle("RACOON-AI")

        self._set_texts()
        self._set_images()

        self.__grid = QGridLayout()
        self.__grid.addWidget(self.__field, 0, 0)
        self.__grid.addWidget(self.__robot, 0, 0)
        self._set_charts()
        self.setLayout(self.__grid)

        self.show()

    def _set_texts(self):
        self.__ai_text = QLabel("RACOON-AI", self)
        self.__ai_text.setGeometry(0, 0, 150, 50)
        self.__ai_text.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__ai_text.setStyleSheet("background-color: white")
        self.__ai_text.setStyleSheet("QLabel { color : white; }")
        self.__ai_text.move(50, -5)

        self.__speed_text = QLabel("Ball Speed", self)
        self.__speed_text.setGeometry(0, 0, 150, 50)
        self.__speed_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__speed_text.setStyleSheet("background-color: white")
        self.__speed_text.setStyleSheet("QLabel { color : white; }")
        self.__speed_text.move(600, 400)

    def _set_images(self):
        self.__pixmap_racoon = QPixmap("images/racoon2.png")
        self.__pixmap_game = QPixmap("images/game_2.png")
        self.__pixmap_block = QPixmap("images/block.png")
        self.__pixmap_referee = QPixmap("images/referee.png")
        self.__pixmap_gear = QPixmap("images/gear.png")

    def active(self) -> None:
        self.update()

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
        self.__ui.drawPixmap(2, 148, 42, 40, self.__pixmap_referee)
        self.__ui.drawPixmap(0, 198, 45, 45, self.__pixmap_gear)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(590, 425, 840, 350)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(600, 425, 705, 425)

        self.__ui.end()

    def _set_charts(self) -> None:
        self.graphWidget = pg.PlotWidget(self)
        self.graphWidget.setGeometry(600, 450, 820, 320)
        self.graphWidget.setBackground(QColor("#2E333A"))
        self.x = list(range(100))
        self.y = [randint(0, 100) for _ in range(100)]

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self) -> None:
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)
