#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""main.py

    This module is for the Main class.
"""
import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QLabel, QWidget

from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Main(QWidget):
    """Main
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: MWReceiver, role: Role) -> None:
        super(Main, self).__init__()
        self.__geometry_width: int = 590
        self.__geometry_height: int = 850

        self.__observer: MWReceiver = observer
        self.__role: Role = role

        self._initui()

    def _initui(self) -> None:
        self.resize(self.__geometry_width, self.__geometry_height)
        self.setWindowTitle("RACOON-AI")

        self._set_images()
        self._set_num()

    def _set_images(self):
        self.__pixmap_racoon = QPixmap("racoon_ai/gui/images/racoon2.png")
        self.__pixmap_game = QPixmap("racoon_ai/gui/images/game_2.png")
        self.__pixmap_block = QPixmap("racoon_ai/gui/images/block.png")
        self.__pixmap_referee = QPixmap("racoon_ai/gui/images/referee.png")
        self.__pixmap_gear = QPixmap("racoon_ai/gui/images/gear.png")
        self.__pixmap_role = QPixmap("racoon_ai/gui/images/role_table.png")

    def _set_num(self):
        self.__keeper_num = QLabel(self)
        self.__keeper_num.setFont(QFont("Arial", 30))

        self.__midfielder_num = QLabel(self)
        self.__midfielder_num.setFont(QFont("Arial", 30))

        self.__offense_num = []
        self.__defense_num = []
        for i in range(3):
            self.__offense_num.append(QLabel(self))
            self.__offense_num[i].setFont(QFont("Arial", 30))
            self.__defense_num.append(QLabel(self))
            self.__defense_num[i].setFont(QFont("Arial", 30))

        self.__fps_num = QLabel(self)
        self.__fps_num.setFont(QFont("Arial", 16))
        self.__fps_num.setGeometry(100, 100, 200, 200)
        self.__fps_num.move(707, 160)

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

        self.__ui.setPen(QColor("white"))
        self.__ui.setBrush(QColor("gray"))
        # Feild全体
        self.__ui.drawRect(47, 42, 520, 730)
        # Feild line
        self.__ui.drawRect(87, 82, 440, 650)
        # Center line
        self.__ui.drawEllipse(282, 362, 30, 30)
        # Down Goal line
        self.__ui.drawRect(242, 672, 120, 60)
        # Up Goal line
        self.__ui.drawRect(242, 82, 120, 60)
        # Down Goal
        self.__ui.drawRect(272, 731, 60, 10)
        # Up Goal
        self.__ui.drawRect(272, 72, 60, 10)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(586, 425, 840, 350)  # Ball of the rectangle
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(600, 425, 705, 425)

        self.__ui.setBrush(QColor("orange"))
        self.__ui.drawEllipse(
            int((self.__observer.ball.y * 0.05) + 302), int((self.__observer.ball.x * 0.05) + 392), 2, 2
        )
        self._draw_robots("blue", self.__ui)
        self._draw_robots("yellow", self.__ui)
        self._draw_role(self.__ui)

        self.__ui.drawPixmap(590, 297, 550, 115, self.__pixmap_role)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(822, 57, 310, 95)  # To draw of robot
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(832, 57, 962, 57)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(822, 167, 180, 115)  # To draw of Control Robot
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(832, 167, 944, 167)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(1014, 167, 125, 115)  # To draw of Camera
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(1019, 167, 1074, 167)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(588, 57, 222, 225)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(599, 57, 662, 57)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(1152, 57, 270, 355)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(1167, 57, 1312, 57)

        self.__fps_num.setNum(60)

        self.__ui.end()

    def _draw_robots(self, color: str, ui: QPainter) -> None:
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
                    int(((robot.y * 0.05) + 302) - 6),
                    int(((robot.x * 0.05) + 392) - 7),
                    14,
                    14,
                    int((math.degrees(robot.theta) + 342) * 16),
                    302 * 16,
                )
                self.__ui.setPen(QColor(Qt.white))
                self.__ui.drawLine(
                    int(((robot.y * 0.05) + 302)),
                    int(((robot.x * 0.05) + 392)),
                    int((((robot.y * 0.05) + 302)) - 4 * math.cos(-robot.theta - math.pi / 2)),
                    int((((robot.x * 0.05) + 392)) - 4 * math.sin(-robot.theta - math.pi / 2)),
                )

    def _draw_role(self, ui: QPainter) -> None:
        ui.setBrush(QColor("#2E333A"))
        ui.setPen(QColor("white"))
        ui.drawRect(588, 297, 553, 115)  # To draw of role
        ui.setPen(QColor("#2E333A"))
        ui.drawLine(602, 297, 647, 297)

        self.__keeper_num.setGeometry(20, 20, 645, 70)
        self.__keeper_num.move(675, 319)
        self.__keeper_num.setNum(self.__role.keeper_id)
        self.__midfielder_num.setGeometry(20, 20, 645, 70)
        self.__midfielder_num.move(1100, 319)
        self.__midfielder_num.setNum(self.__role.midfielder_id)
        for i in range(3):
            self.__offense_num[i].setGeometry(20, 20, 645, 70)
            self.__offense_num[i].move(735 + (61 * i), 319)
            self.__offense_num[i].setNum(self.__role.offense_ids[i])

            self.__defense_num[i].setGeometry(20, 20, 645, 70)
            self.__defense_num[i].move(918 + (61 * i), 319)
            self.__defense_num[i].setNum(self.__role.defense_ids[i])
