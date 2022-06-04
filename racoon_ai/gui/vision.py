#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""vision.py

    This module is for the Vision class.
"""
from PyQt5 import QtGui
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QComboBox, QLabel, QSpinBox
from qtwidgets import AnimatedToggle

from racoon_ai.gui.main import Main


class Vision:
    """Vision
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        super(Vision, self).__init__()
        self.__main = main

        self._set_texts()
        self._set_box()
        self._set_toggle()

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self.__main)
        self.__ui.setBrush(QColor("orange"))

        self.__ui.end()

    def _set_texts(self) -> None:
        self.__role_text = QLabel("Vision", self.__main)
        self.__role_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__role_text.setStyleSheet("QLabel { color : white; }")
        self.__role_text.move(601, 44)

        self.__simu_text = QLabel("Simu", self.__main)
        self.__simu_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(602, 82)
        self.__real_text = QLabel("Real", self.__main)
        self.__real_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(760, 80)

        self.__simu_text = QLabel("Blue", self.__main)
        self.__simu_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(602, 126)
        self.__real_text = QLabel("Yellow", self.__main)
        self.__real_text.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(757, 126)

        self.__receive_text = QLabel("Receive Port:", self.__main)
        self.__receive_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__receive_text.setStyleSheet("QLabel { color : white; }")
        self.__receive_text.move(602, 170)

        self.__send_text = QLabel("Send Port:", self.__main)
        self.__send_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__send_text.setStyleSheet("QLabel { color : white; }")
        self.__send_text.move(620, 198)

        self.__camera_text = QLabel("Camera Num:", self.__main)
        self.__camera_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__camera_text.setStyleSheet("QLabel { color : white; }")
        self.__camera_text.move(600, 224)

        self.__fps_text = QLabel("Vision Fps:", self.__main)
        self.__fps_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        self.__fps_text.setStyleSheet("QLabel { color : white; }")
        self.__fps_text.move(615, 250)

    def _set_toggle(self) -> None:
        toggle = AnimatedToggle(
            self.__main,
            bar_color="#224726",
            handle_color="#57BD37",
            checked_color="#3F3F3F",
            pulse_unchecked_color="#57BD37",
            pulse_checked_color="#3F3F3F",
        )
        toggle.resize(120, 60)
        toggle.move(640, 68)
        toggle_color = AnimatedToggle(
            self.__main,
            bar_color="#0000D6",
            handle_color="#00B0FF",
            checked_color="#D6D600",
            pulse_unchecked_color="#00B0FF",
            pulse_checked_color="#D6D600",
        )
        toggle_color.resize(120, 60)
        toggle_color.move(640, 114)

    def _set_box(self) -> None:
        receive_box = QSpinBox(self.__main)
        receive_box.resize(70, 20)
        receive_box.setMaximum(20000)
        receive_box.setMinimum(10020)
        receive_box.move(702, 169)

        send_box = QSpinBox(self.__main)
        send_box.resize(70, 20)
        send_box.setMaximum(30000)
        send_box.setMinimum(20020)
        send_box.move(702, 197)

        camera_box = QSpinBox(self.__main)
        camera_box.resize(70, 20)
        camera_box.setMaximum(4)
        camera_box.setMinimum(1)
        camera_box.move(702, 223)

        combo = QComboBox(self.__main)
        combo.addItem("NORMAL")
        combo.addItem("Swirl")
        combo.resize(120, 140)
        combo.move(1017, 167)
