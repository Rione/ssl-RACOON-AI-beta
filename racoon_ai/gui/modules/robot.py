#!/usr/bin/env python3.10

"""field.py

    This module is for the Feild class.
"""

from PySide6.QtGui import QFont  # pylint: disable=E0611
from PySide6.QtWidgets import QCheckBox, QLabel, QSpinBox  # pylint: disable=E0611

from .animated_toggle import AnimatedToggle
from .main import Main


class Robot:  # pylint: disable=R0903
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        self.__main: Main = main
        self.__role_text: QLabel
        self.__robot_text: QLabel
        self.__camera_active_text: QLabel
        self.__robot_num_text: QLabel
        self.__joy_enable_text: QLabel
        self.__joy_robot_text: QLabel
        self.__joy_status_text: QLabel
        self.__joy_connect_text: QLabel
        self.__set_texts()
        self.__set_box()
        self.__set_toggle()

    def __set_box(self) -> None:
        robot_check: list[QCheckBox] = []
        for i in range(16):
            robot_check.append(QCheckBox(self.__main))
            if i < 8:
                robot_check[i].move(842 + i * 35, 82)
            else:
                robot_check[i].move(842 + (i - 8) * 35, 112)

        # robot_check = []
        # for i in range(8):
        #     robot_check.append(QCheckBox(self))
        #     if i < 4:
        #         robot_check[i].move(1008 + i * 28, 169)
        #     else:
        #         robot_check[i].move(1008 + (i - 4) * 28, 209)

        robot_number = QSpinBox(self.__main)
        robot_number.resize(70, 20)
        robot_number.setMaximum(15)
        robot_number.setMinimum(0)
        robot_number.move(922, 228)

    def __set_texts(self) -> None:  # pylint: disable=R0915
        self.__role_text = QLabel("Role", self.__main)
        self.__role_text.setFont(QFont("Arial", 20))
        self.__role_text.setStyleSheet("QLabel { color : white; }")
        self.__role_text.move(602, 284)

        self.__robot_text = QLabel("Active Robot", self.__main)
        self.__robot_text.setFont(QFont("Arial", 20))
        self.__robot_text.setGeometry(10, 10, 600, 36)
        self.__robot_text.setStyleSheet("QLabel { color : white; }")
        self.__robot_text.move(834, 40)

        self.__camera_active_text = QLabel("Mode", self.__main)
        self.__camera_active_text.setFont(QFont("Arial", 20))
        self.__camera_active_text.setStyleSheet("QLabel { color : white; }")
        self.__camera_active_text.move(1020, 154)

        for num in range(16):
            self.__robot_num_text = QLabel(str(num), self.__main)
            self.__robot_num_text.setFont(QFont("Arial", 14))
            self.__robot_num_text.setStyleSheet("QLabel { color : white; }")
            if num < 8:
                self.__robot_num_text.move(832 + num * 35, 83)
            else:
                increase = 0
                if num >= 10:
                    increase = -6
                self.__robot_num_text.move(832 + (num - 8) * 35 + increase, 113)
        # camera_num = ["0", "1", "2", "3", "4", "5", "6", "7"]
        # count = -1
        # for num in camera_num:
        #     count = count + 1
        #     self.__camera_num_text = QLabel(num, self)
        #     self.__camera_num_text.setFont(QFont("Arial", 14, QFont.Black))
        #     self.__camera_num_text.setStyleSheet("QLabel { color : white; }")
        #     if count < 4:
        #         self.__camera_num_text.move(1000 + count * 28, 170)
        #     else:
        #         self.__camera_num_text.move(1000 + (count - 4) * 28, 210)

        self.__robot_text = QLabel("Joy Control", self.__main)
        self.__robot_text.setFont(QFont("Arial", 20))
        self.__robot_text.setGeometry(10, 10, 600, 156)
        self.__robot_text.setStyleSheet("QLabel { color : white; }")
        self.__robot_text.move(834, 88)

        self.__joy_enable_text = QLabel("JoyStick :", self.__main)
        self.__joy_enable_text.setFont(QFont("Arial", 17))
        self.__joy_enable_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_enable_text.move(837, 190)

        self.__joy_robot_text = QLabel("Number :", self.__main)
        self.__joy_robot_text.setFont(QFont("Arial", 17))
        self.__joy_robot_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_robot_text.move(842, 224)
        self.__joy_status_text = QLabel("Connect :", self.__main)
        self.__joy_status_text.setFont(QFont("Arial", 17))
        self.__joy_status_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_status_text.move(838, 252)
        self.__joy_connect_text = QLabel("OK", self.__main)
        self.__joy_connect_text.setFont(QFont("Arial", 17))
        self.__joy_connect_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_connect_text.move(927, 252)
        self.__joy_connect_text = QLabel("Kill:", self.__main)
        self.__joy_connect_text.setFont(QFont("Arial", 18))
        self.__joy_connect_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_connect_text.move(1044, 254)
        self.__joy_enable_text = QLabel("Status:", self.__main)
        self.__joy_enable_text.setFont(QFont("Arial", 17))
        self.__joy_enable_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_enable_text.move(1022, 190)

    def __set_toggle(self) -> None:
        # pylint: disable=R0801
        joystick = AnimatedToggle(
            self.__main,
            bar_color="#0000D6",
            handle_color="#00B0FF",
            checked_color="#D6D600",
            pulse_unchecked_color="#00B0FF",
            pulse_checked_color="#D6D600",
        )
        joystick.resize(80, 50)
        joystick.move(915, 178)

        mode = AnimatedToggle(
            self.__main,
            bar_color="#0000D6",
            handle_color="#00B0FF",
            checked_color="#D6D600",
            pulse_unchecked_color="#00B0FF",
            pulse_checked_color="#D6D600",
        )
        mode.resize(70, 50)
        mode.move(1075, 178)

        mode = AnimatedToggle(
            self.__main,
            bar_color="#5E5E5E",
            handle_color="#3F3F3F",
            checked_color="#D6D600",
            pulse_unchecked_color="#00B0FF",
            pulse_checked_color="#D6D600",
        )
        mode.resize(70, 50)
        mode.move(1075, 238)
