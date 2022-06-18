#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""chart.py

    This module is for the Chart class.
"""

import pyqtgraph as pg
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QLabel

from racoon_ai.gui.main import Main
from racoon_ai.networks.receiver import MWReceiver


class Chart:
    """Chart
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main, observer: MWReceiver) -> None:
        super(Chart, self).__init__()
        self.__observer: MWReceiver = observer
        self.__main = main
        self._set_text()
        self._set_charts()

    def _set_text(self) -> None:
        self.__speed_text = QLabel("Ball Speed", self.__main)
        self.__speed_text.setGeometry(0, 0, 150, 50)
        self.__speed_text.setFont(QtGui.QFont("Arial", 20))
        self.__speed_text.setStyleSheet("background-color: white")
        self.__speed_text.setStyleSheet("QLabel { color : white; }")
        self.__speed_text.move(600, 400)

    def _set_charts(self) -> None:
        self.graphWidget = pg.PlotWidget(self.__main)
        self.graphWidget.setGeometry(600, 450, 820, 320)
        self.graphWidget.setBackground(QColor("#2E333A"))
        self.x = list(range(120))
        self.y = [0 for _ in range(120)]

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer(self.__main)
        self.timer.setInterval(50)
        #self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self) -> None:

        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]  # Remove the first

        self.y.append(self.__observer.ball.speed)  # Add a new random value.

        self.data_line.setData(self.x, self.y)
