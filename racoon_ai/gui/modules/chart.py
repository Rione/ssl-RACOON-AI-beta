#!/usr/bin/env python3.10

"""chart.py

    This module is for the Chart class.
"""

from itertools import repeat

from pyqtgraph import PlotWidget, mkPen  # type: ignore
from PySide6.QtCore import QTimer  # pylint: disable=E0611
from PySide6.QtGui import QColor, QFont  # pylint: disable=E0611
from PySide6.QtWidgets import QLabel  # pylint: disable=E0611

from racoon_ai.networks.receiver import MWReceiver

from .main import Main


class Chart:  # pylint: disable=R0903
    """Chart
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main, observer: MWReceiver) -> None:
        self.__observer: MWReceiver = observer
        self.__main: Main = main
        self.graphWidget: PlotWidget = PlotWidget(self.__main)  # pylint: disable=C0103
        self.__speed_text: QLabel
        self.x: list[float]
        self.y: list[float]
        self.timer: QTimer
        self._set_text()
        self._set_charts()

    def _set_text(self) -> None:
        self.__speed_text = QLabel("Ball Speed", self.__main)
        self.__speed_text.setGeometry(0, 0, 150, 50)
        self.__speed_text.setFont(QFont("Arial", 20))
        self.__speed_text.setStyleSheet("background-color: white")
        self.__speed_text.setStyleSheet("QLabel { color : white; }")
        self.__speed_text.move(600, 400)

    def _set_charts(self) -> None:
        self.graphWidget.setGeometry(600, 450, 820, 320)
        self.graphWidget.setBackground(QColor("#2E333A"))
        self.x = list(range(120))
        self.y = list(repeat(float(0), 120))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=mkPen(color=(255, 0, 0)))
        self.timer = QTimer(self.__main)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)  # type: ignore
        self.timer.start()

    def update_plot_data(self) -> None:
        """update_plot_data"""
        self.x = self.x[1:]
        self.x.append(self.x[-1] + 1)

        self.y = self.y[1:]  # Remove the first
        self.y.append(self.__observer.ball.speed)  # Add a new random value.
        self.data_line.setData(self.x, self.y)
