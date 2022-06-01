#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""field.py

    This module is for the Feild class.
"""
import math

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Robot(QWidget, QPainter):
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: MWReceiver, role: Role) -> None:
        super(Robot, self).__init__()
        self.__ui: QPainter()
        self.__observer: MWReceiver = observer
        self.__role: Role = role

        self._set_texts()

        self.__geometry_width: int = 720
        self.__geometry_height: int = 850
        self.__window_width: float = 1.0
        self.__window_height: float = 1.0

        self.__keeper_num = QLabel(self)
        self.__keeper_num.setFont(QFont("Arial", 30, QFont.Bold))

        self.__midfielder_num = QLabel(self)
        self.__midfielder_num.setFont(QFont("Arial", 30, QFont.Bold))

        self.__offense_num = []
        self.__defense_num = []
        for i in range(3):
            self.__offense_num.append(QLabel(self))
            self.__offense_num[i].setFont(QFont("Arial", 30, QFont.Bold))
            self.__defense_num.append(QLabel(self))
            self.__defense_num[i].setFont(QFont("Arial", 30, QFont.Bold))

        self.__pixmap_role = QPixmap("images/role_table.png")

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)
        self.__ui.setBrush(QColor("orange"))
        self.__ui.drawEllipse(
            int((self.__observer.ball.y * 0.05) + 280), int((self.__observer.ball.x * 0.05) + 370), 2, 2
        )

        self._draw_robots("blue")
        self._draw_robots("yellow")
        self._draw_role()

        self.__ui.drawPixmap(560, 30, 550, 115, self.__pixmap_role)
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
        self.__ui.drawRect(560, 30, 551, 115)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(570, 30, 615, 30)

        self.__role_text.move(570, 18)

        self.__keeper_num.setGeometry(20, 20, 645, 70)
        self.__keeper_num.move(645, 52)
        self.__keeper_num.setNum(self.__role.keeper_id)
        self.__midfielder_num.setGeometry(20, 20, 645, 70)
        self.__midfielder_num.move(1070, 52)
        self.__midfielder_num.setNum(self.__role.midfielder_id)
        for i in range(3):
            self.__offense_num[i].setGeometry(20, 20, 645, 70)
            self.__offense_num[i].move(705 + (61 * i), 52)
            self.__offense_num[i].setNum(self.__role.offense_ids[i])

            self.__defense_num[i].setGeometry(20, 20, 645, 70)
            self.__defense_num[i].move(888 + (61 * i), 52)
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
        self.__role_text = QLabel("Role", self)
        self.__role_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__role_text.setStyleSheet("QLabel { color : white; }")
