#!/usr/bin/env python3.10

"""vision.py

    This module is for the Vision class.
"""

from PyQt6.QtGui import QColor, QFont, QPainter, QPaintEvent  # pylint: disable=E0611
from PyQt6.QtWidgets import QComboBox, QLabel, QSpinBox  # pylint: disable=E0611

from .animated_toggle import AnimatedToggle
from .main import Main


class Vision:  # pylint: disable=R0903
    """Vision
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        self.__main: Main = main
        self.__ui = QPainter(self.__main)
        self.__role_text: QLabel
        self.__simu_text: QLabel
        self.__real_text: QLabel
        self.__receive_text: QLabel
        self.__send_text: QLabel
        self.__camera_text: QLabel
        self.__fps_text: QLabel
        self.__set_texts()
        self.__set_box()
        self.__set_toggle()

    def paintEvent(self, _: QPaintEvent) -> None:  # pylint: disable=C0103
        """paintEvent"""
        self.__ui.setBrush(QColor("orange"))
        self.__ui.end()

    def __set_texts(self) -> None:
        self.__role_text = QLabel("Vision", self.__main)
        self.__role_text.setFont(QFont("Arial", 20))
        self.__role_text.setStyleSheet("QLabel { color : white; }")
        self.__role_text.move(601, 44)

        self.__simu_text = QLabel("Simu", self.__main)
        self.__simu_text.setFont(QFont("Arial", 15))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(602, 82)
        self.__real_text = QLabel("Real", self.__main)
        self.__real_text.setFont(QFont("Arial", 15))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(760, 80)

        self.__simu_text = QLabel("Blue", self.__main)
        self.__simu_text.setFont(QFont("Arial", 15))
        self.__simu_text.setStyleSheet("QLabel { color : white; }")
        self.__simu_text.move(602, 126)
        self.__real_text = QLabel("Yellow", self.__main)
        self.__real_text.setFont(QFont("Arial", 15))
        self.__real_text.setStyleSheet("QLabel { color : white; }")
        self.__real_text.move(757, 126)

        self.__receive_text = QLabel("Receive Port:", self.__main)
        self.__receive_text.setFont(QFont("Arial", 14))
        self.__receive_text.setStyleSheet("QLabel { color : white; }")
        self.__receive_text.move(602, 170)

        self.__send_text = QLabel("Send Port:", self.__main)
        self.__send_text.setFont(QFont("Arial", 14))
        self.__send_text.setStyleSheet("QLabel { color : white; }")
        self.__send_text.move(620, 198)

        self.__camera_text = QLabel("Camera Num:", self.__main)
        self.__camera_text.setFont(QFont("Arial", 14))
        self.__camera_text.setStyleSheet("QLabel { color : white; }")
        self.__camera_text.move(600, 224)

        self.__fps_text = QLabel("Vision Fps:", self.__main)
        self.__fps_text.setFont(QFont("Arial", 14))
        self.__fps_text.setStyleSheet("QLabel { color : white; }")
        self.__fps_text.move(615, 250)

    def __set_toggle(self) -> None:
        # pylint: disable=R0801
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

    def __set_box(self) -> None:
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
