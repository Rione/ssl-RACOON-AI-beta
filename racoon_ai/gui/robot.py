#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""field.py

    This module is for the Feild class.
"""
import math
from ast import increment_lineno

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt5.QtWidgets import QCheckBox, QLabel, QSpinBox, QWidget

from racoon_ai.gui.main import Gui
from racoon_ai.models import robot
from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Robot:
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, gui: Gui, observer: MWReceiver, role: Role) -> None:
        self.__ui: QPainter(self.__gui)
        self.__gui = gui
        self.__observer: MWReceiver = observer
        self.__role: Role = role

        self._set_texts()

        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__window_width: float = 1.0
        self.__window_height: float = 1.0

        self.__keeper_num = QLabel(self.__gui)
        self.__keeper_num.setFont(QFont("Arial", 30, QFont.Bold))

        self.__midfielder_num = QLabel(self.__gui)
        self.__midfielder_num.setFont(QFont("Arial", 30, QFont.Bold))

        self.__offense_num = []
        self.__defense_num = []
        for i in range(3):
            self.__offense_num.append(QLabel(self.__gui))
            self.__offense_num[i].setFont(QFont("Arial", 30, QFont.Bold))
            self.__defense_num.append(QLabel(self.__gui))
            self.__defense_num[i].setFont(QFont("Arial", 30, QFont.Bold))

        self.__pixmap_role = QPixmap("images/role_table.png")
        self.__pixmap_stop = QPixmap("images/stop.png")

        robot_check = []
        for i in range(16):
            robot_check.append(QCheckBox(self.__gui))
            if i < 8:
                robot_check[i].move(820 + i * 35, 60)
            else:
                robot_check[i].move(820 + (i - 8) * 35, 90)

        # robot_check = []
        # for i in range(8):
        #     robot_check.append(QCheckBox(self))
        #     if i < 4:
        #         robot_check[i].move(1008 + i * 28, 169)
        #     else:
        #         robot_check[i].move(1008 + (i - 4) * 28, 209)

        robot_number = QSpinBox(self.__gui)
        robot_number.resize(70, 20)
        robot_number.setMaximum(15)
        robot_number.setMinimum(0)
        robot_number.move(900, 202)

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self.__gui)
        self.__ui.setBrush(QColor("orange"))
        self.__ui.drawEllipse(
            int((self.__observer.ball.y * 0.05) + 280), int((self.__observer.ball.x * 0.05) + 370), 2, 2
        )

        self._draw_robots("blue")
        self._draw_robots("yellow")
        self._draw_role()

        self.__ui.drawPixmap(568, 275, 550, 115, self.__pixmap_role)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(800, 35, 310, 95)  # To draw of robot
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(810, 35, 940, 35)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(800, 145, 180, 115)  # To draw of Control Robot
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(810, 145, 922, 145)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(992, 145, 125, 115)  # To draw of Camera
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(997, 145, 1052, 145)

        self.__ui.end()

    def _draw_robots(self, color: str) -> None:
        if color == "blue":
            self.__ui.setBrush(QColor("blue"))
            robots = self.__observer.our_robots
        else:
            self.__ui.setBrush(QColor("yellow"))
            robots = self.__observer.enemy_robots

        for robot in robots:
            if robot.x != 0:
                self.__ui.setPen(QColor(Qt.black))
                self.__ui.drawChord(
                    int(((robot.y * 0.05) + 280) - 6),
                    int(((robot.x * 0.05) + 370) - 7),
                    14,
                    14,
                    int((math.degrees(robot.theta) + 320) * 16),
                    280 * 16,
                )
                self.__ui.setPen(QColor(Qt.white))
                self.__ui.drawLine(
                    int(((robot.y * 0.05) + 280)),
                    int(((robot.x * 0.05) + 370)),
                    int((((robot.y * 0.05) + 280)) - 4 * math.cos(-robot.theta - math.pi / 2)),
                    int((((robot.x * 0.05) + 370)) - 4 * math.sin(-robot.theta - math.pi / 2)),
                )

    def _draw_role(self) -> None:
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(566, 275, 553, 115)  # To draw of role
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(580, 275, 625, 275)

        self.__role_text.move(580, 262)

        self.__keeper_num.setGeometry(20, 20, 645, 70)
        self.__keeper_num.move(653, 297)
        self.__keeper_num.setNum(self.__role.keeper_id)
        self.__midfielder_num.setGeometry(20, 20, 645, 70)
        self.__midfielder_num.move(1078, 297)
        self.__midfielder_num.setNum(self.__role.midfielder_id)
        for i in range(3):
            self.__offense_num[i].setGeometry(20, 20, 645, 70)
            self.__offense_num[i].move(713 + (61 * i), 297)
            self.__offense_num[i].setNum(self.__role.offense_ids[i])

            self.__defense_num[i].setGeometry(20, 20, 645, 70)
            self.__defense_num[i].move(896 + (61 * i), 297)
            self.__defense_num[i].setNum(self.__role.defense_ids[i])

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

    def _set_texts(self) -> None:
        self.__role_text = QLabel("Role", self.__gui)
        self.__role_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__role_text.setStyleSheet("QLabel { color : white; }")

        self.__robot_text = QLabel("Active Robot", self.__gui)
        self.__robot_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__robot_text.setStyleSheet("QLabel { color : white; }")
        self.__robot_text.move(810, 24)

        self.__camera_active_text = QLabel("Mode", self.__gui)
        self.__camera_active_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__camera_active_text.setStyleSheet("QLabel { color : white; }")
        self.__camera_active_text.move(998, 132)

        robot_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
        count = -1
        for num in robot_num:
            count = count + 1
            self.__robot_num_text = QLabel(num, self.__gui)
            self.__robot_num_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
            self.__robot_num_text.setStyleSheet("QLabel { color : white; }")
            if count < 8:
                self.__robot_num_text.move(810 + count * 35, 61)
            else:
                increase = 0
                if count >= 10:
                    increase = -6
                self.__robot_num_text.move(810 + (count - 8) * 35 + increase, 91)
        # camera_num = ["0", "1", "2", "3", "4", "5", "6", "7"]
        # count = -1
        # for num in camera_num:
        #     count = count + 1
        #     self.__camera_num_text = QLabel(num, self)
        #     self.__camera_num_text.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))
        #     self.__camera_num_text.setStyleSheet("QLabel { color : white; }")
        #     if count < 4:
        #         self.__camera_num_text.move(1000 + count * 28, 170)
        #     else:
        #         self.__camera_num_text.move(1000 + (count - 4) * 28, 210)

        self.__robot_text = QLabel("Joy Control", self.__gui)
        self.__robot_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__robot_text.setStyleSheet("QLabel { color : white; }")
        self.__robot_text.move(810, 134)

        self.__joy_enable_text = QLabel("JoyStick :", self.__gui)
        self.__joy_enable_text.setFont(QtGui.QFont("Arial", 17, QtGui.QFont.Black))
        self.__joy_enable_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_enable_text.move(815, 168)

        self.__joy_robot_text = QLabel("Number :", self.__gui)
        self.__joy_robot_text.setFont(QtGui.QFont("Arial", 17, QtGui.QFont.Black))
        self.__joy_robot_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_robot_text.move(820, 202)
        self.__joy_status_text = QLabel("Connect :", self.__gui)
        self.__joy_status_text.setFont(QtGui.QFont("Arial", 17, QtGui.QFont.Black))
        self.__joy_status_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_status_text.move(816, 230)
        self.__joy_connect_text = QLabel("OK", self.__gui)
        self.__joy_connect_text.setFont(QtGui.QFont("Arial", 17, QtGui.QFont.Black))
        self.__joy_connect_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_connect_text.move(905, 230)
        self.__joy_connect_text = QLabel("Kill:", self.__gui)
        self.__joy_connect_text.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__joy_connect_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_connect_text.move(1022, 226)
        self.__joy_enable_text = QLabel("Status:", self.__gui)
        self.__joy_enable_text.setFont(QtGui.QFont("Arial", 17, QtGui.QFont.Black))
        self.__joy_enable_text.setStyleSheet("QLabel { color : white; }")
        self.__joy_enable_text.move(1000, 168)
