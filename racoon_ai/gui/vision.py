#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""vision.py

    This module is for the Vision class.
"""
import math

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt5.QtWidgets import QComboBox, QLabel, QSpinBox, QVBoxLayout, QWidget
from qtwidgets import AnimatedToggle, EqualizerBar, Toggle

from racoon_ai.gui.main import Gui
from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Vision(Gui):
    """Vision
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: MWReceiver, role: Role) -> None:
        self.__ui: QPainter(self)
        self.__observer: MWReceiver = observer

        self._set_texts()

        receive_box = QSpinBox(self)
        receive_box.resize(70, 20)
        receive_box.setMaximum(20000)
        receive_box.setMinimum(10020)
        receive_box.move(680, 142)

        send_box = QSpinBox(self)
        send_box.resize(70, 20)
        send_box.setMaximum(30000)
        send_box.setMinimum(20020)
        send_box.move(680, 170)

        camera_box = QSpinBox(self)
        camera_box.resize(70, 20)
        camera_box.setMaximum(4)
        camera_box.setMinimum(1)
        camera_box.move(680, 196)

        self.__fps_num = QLabel(self)
        self.__fps_num.setFont(QFont("Arial", 16, QFont.Bold))
        self.__fps_num.setGeometry(100, 100, 200, 200)
        self.__fps_num.move(684, 132)

        combo = QComboBox(self)
        combo.addItem("NORMAL")
        combo.addItem("Swirl")
        combo.resize(120, 140)
        combo.move(995, 140)

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)
        self.__ui.setBrush(QColor("orange"))

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(566, 35, 222, 225)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(577, 35, 640, 35)

        self.__fps_num.setNum(60)

        self.__ui.end()

    def _set_texts(self) -> None:
        self.__role_text = QLabel("Vision", self)
        self.__role_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__role_text.setStyleSheet("QLabel { color : white; }")
        self.__role_text.move(579, 22)

        self.__simu_text = QLabel("Simu", self)
        self.__simu_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(580, 60)
        self.__real_text = QLabel("Real", self)
        self.__real_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(738, 58)

        self.__simu_text = QLabel("Blue", self)
        self.__simu_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(580, 104)
        self.__real_text = QLabel("Yellow", self)
        self.__real_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(735, 104)

        self.__receive_text = QLabel("Receive Port:", self)
        self.__receive_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__receive_text.setStyleSheet("QLabel { color : white; }")
        self.__receive_text.move(580, 142)

        self.__send_text = QLabel("Send Port:", self)
        self.__send_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__send_text.setStyleSheet("QLabel { color : white; }")
        self.__send_text.move(598, 170)

        self.__camera_text = QLabel("Camera Num:", self)
        self.__camera_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__camera_text.setStyleSheet("QLabel { color : white; }")
        self.__camera_text.move(578, 196)

        self.__fps_text = QLabel("Vision Fps:", self)
        self.__fps_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__fps_text.setStyleSheet("QLabel { color : white; }")
        self.__fps_text.move(593, 222)
