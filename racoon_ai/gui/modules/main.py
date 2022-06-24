#!/usr/bin/env python3.10

"""main.py
    This module is for the Main class.
"""

from math import cos, degrees, radians, sin

from PySide6.QtCore import QPoint, QPointF, QRectF  # pylint: disable=E0611
from PySide6.QtGui import QColor, QFont, QPainter, QPaintEvent, QPixmap  # pylint: disable=E0611
from PySide6.QtWidgets import QLabel, QMainWindow  # pylint: disable=E0611

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.observer import Observer
from racoon_ai.strategy import Role


class Main(QMainWindow):
    """Main
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: Observer, role: Role) -> None:
        super().__init__()

        self.__observer: Observer = observer
        self.__role: Role = role

        self.__ui: QPainter
        self.__geometry_width: int = 1450
        self.__geometry_height: int = 850

        self.__field_length: int = 687
        self.__field_width: int = 483

        self.__robot_radius: int = 100
        self.__ball_radius: int = 40

        self.__wall_corner: QPoint = QPoint(48, 43)
        self.__wall_to_line_length: int = 300

        self.__shrink_length: float = self.__field_length / self.__observer.geometry.field_length
        self.__shrink_width: float = self.__field_width / self.__observer.geometry.field_width
        self.__shrink_ratio: float = (self.__shrink_length + self.__shrink_width) / 2.0

        self.__field_corner: QPoint = QPoint(
            int(self.__wall_corner.x() + self.__wall_to_line_length * self.__shrink_width),
            int(self.__wall_corner.y() + self.__wall_to_line_length * self.__shrink_length),
        )
        self.__field_center: QPoint = QPoint(
            int(self.__field_width / 2.0 + self.__field_corner.x()),
            int(self.__field_length / 2.0 + self.__field_corner.y()),
        )

        self.__center_circle_radius = int(500 * self.__shrink_ratio)

        self.__pixmap_racoon: QPixmap
        self.__pixmap_game: QPixmap
        self.__pixmap_block: QPixmap
        self.__pixmap_referee: QPixmap
        self.__pixmap_gear: QPixmap
        self.__pixmap_role: QPixmap

        self.__keeper_num: QLabel
        self.__midfielder_num: QLabel
        self.__offense_num: list[QLabel]
        self.__defense_num: list[QLabel]

        self.__fps_num: QLabel

        self._initui()

    def _initui(self) -> None:
        self.resize(self.__geometry_width, self.__geometry_height)
        self.setWindowTitle("RACOON-AI")
        self._set_images()
        self._set_num()

    def _set_images(self) -> None:
        self.__pixmap_racoon = QPixmap("racoon_ai/gui/images/racoon2.png")
        self.__pixmap_game = QPixmap("racoon_ai/gui/images/game_2.png")
        self.__pixmap_block = QPixmap("racoon_ai/gui/images/block.png")
        self.__pixmap_referee = QPixmap("racoon_ai/gui/images/referee.png")
        self.__pixmap_gear = QPixmap("racoon_ai/gui/images/gear.png")
        self.__pixmap_role = QPixmap("racoon_ai/gui/images/role_table.png")

    def _set_num(self) -> None:
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
        """active"""
        self.update()

    def paintEvent(self, _: QPaintEvent) -> None:  # pylint: disable=C0103
        """paintEvent"""
        self.__ui = QPainter(self)

        self._draw_background()
        self._draw_field()
        self._draw_frame()

        self._draw_ball()
        self._draw_robots("blue")
        self._draw_robots("yellow")
        # self._draw_role()

        self.__fps_num.setNum(60)

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
                self.__ui.setPen(QColor("black"))
                self.__ui.drawChord(
                    int(
                        robot.y * self.__shrink_width
                        + self.__field_center.x()
                        - (self.__robot_radius * self.__shrink_width)
                    ),
                    int(
                        robot.x * self.__shrink_length
                        + self.__field_center.y()
                        - (self.__robot_radius * self.__shrink_length)
                    ),
                    int(self.__robot_radius * self.__shrink_width * 2.5),
                    int(self.__robot_radius * self.__shrink_length * 2.5),
                    int(degrees(MU.radian_normalize(robot.theta - radians(45))) * 16),
                    275 * 16,
                )
                if color == "blue":
                    self.__ui.setPen(QColor("white"))
                else:
                    self.__ui.setPen(QColor("black"))
                robot_center_p1 = QPointF(
                    robot.y * self.__shrink_width + self.__field_center.x(),
                    robot.x * self.__shrink_length + self.__field_center.y(),
                )
                robot_center_p2 = QPointF(
                    robot.y * self.__shrink_width
                    + self.__field_center.x()
                    - 4.0 * cos(MU.radian_normalize(-robot.theta - MU.PI / 2)),
                    robot.x * self.__shrink_length
                    + self.__field_center.y()
                    - 4.0 * sin(MU.radian_normalize(-robot.theta - MU.PI / 2)),
                )
                self.__ui.drawLine(robot_center_p1, robot_center_p2)

    def _draw_role(self) -> None:
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(588, 297, 553, 115)  # To draw of role
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(602, 297, 647, 297)

        self.__keeper_num.setGeometry(20, 20, 645, 70)
        self.__keeper_num.move(675, 319)
        self.__keeper_num.setNum(self.__role.keeper_id)
        self.__midfielder_num.setGeometry(20, 20, 645, 70)
        self.__midfielder_num.move(1100, 319)
        # self.__midfielder_num.setNum(1)
        for i in range(3):
            self.__offense_num[i].setGeometry(20, 20, 645, 70)
            self.__offense_num[i].move(735 + (61 * i), 319)
            self.__offense_num[i].setNum(self.__role.get_offense_id(i))

            self.__defense_num[i].setGeometry(20, 20, 645, 70)
            self.__defense_num[i].move(918 + (61 * i), 319)
            self.__defense_num[i].setNum(self.__role.get_defense_id(i))
        self.__ui.drawPixmap(590, 297, 550, 115, self.__pixmap_role)

    def _draw_background(self) -> None:
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

    def _draw_field(self) -> None:
        self.__ui.setPen(QColor("white"))
        self.__ui.setBrush(QColor("gray"))

        self.__ui.drawRect(
            QRectF(
                self.__field_corner.x() - self.__wall_to_line_length * self.__shrink_width,
                self.__field_corner.y() - self.__wall_to_line_length * self.__shrink_length,
                self.__field_width + self.__wall_to_line_length * self.__shrink_width * 2.0,
                self.__field_length + self.__wall_to_line_length * self.__shrink_length * 2.0,
            )
        )

        # Feild line
        self.__ui.drawRect(self.__field_corner.x(), self.__field_corner.y(), self.__field_width, self.__field_length)

        # Center circle

        self.__ui.drawEllipse(self.__field_center, self.__center_circle_radius, self.__center_circle_radius)

        # Up Goal line
        self.__ui.drawRect(
            QRectF(
                self.__field_center.x() - self.__observer.geometry.goal_width * self.__shrink_width,
                self.__field_corner.y(),
                self.__observer.geometry.goal_width * 2.0 * self.__shrink_width,
                self.__observer.geometry.goal_width * self.__shrink_length,
            )
        )
        # Down Goal line
        self.__ui.drawRect(
            QRectF(
                self.__field_center.x() - self.__observer.geometry.goal_width * self.__shrink_width,
                self.__field_corner.y()
                + (self.__observer.geometry.field_length - self.__observer.geometry.goal_width) * self.__shrink_length,
                self.__observer.geometry.goal_width * 2.0 * self.__shrink_width,
                self.__observer.geometry.goal_width * self.__shrink_length,
            )
        )
        # # Up Goal
        self.__ui.drawRect(
            QRectF(
                self.__field_center.x() - self.__observer.geometry.goal_width / 2.0 * self.__shrink_width,
                self.__field_corner.y() - self.__observer.geometry.goal_depth * self.__shrink_length,
                self.__observer.geometry.goal_width * self.__shrink_width,
                self.__observer.geometry.goal_depth * self.__shrink_length,
            )
        )
        # Down Goal
        self.__ui.drawRect(
            QRectF(
                self.__field_center.x() - self.__observer.geometry.goal_width / 2.0 * self.__shrink_width,
                self.__field_corner.y() + self.__observer.geometry.field_length * self.__shrink_length,
                self.__observer.geometry.goal_width * self.__shrink_width,
                self.__observer.geometry.goal_depth * self.__shrink_length,
            )
        )

    def _draw_frame(self) -> None:
        # draw ball speed frame
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(586, 425, 840, 350)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(600, 425, 705, 425)

        # draw robot frame
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(822, 57, 310, 95)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(832, 57, 962, 57)

        # draw control robot frame
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(822, 167, 180, 115)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(832, 167, 944, 167)

        # draw camera frame
        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor("white"))
        self.__ui.drawRect(1014, 167, 125, 115)
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

    def _draw_ball(self) -> None:
        self.__ui.setPen(QColor("red"))
        self.__ui.setBrush(QColor("gray"))
        ball_center = QRectF(
            self.__observer.ball.y * self.__shrink_width
            + self.__field_center.x()
            - self.__ball_radius * self.__shrink_width / 2.0,
            self.__observer.ball.x * self.__shrink_length
            + self.__field_center.y()
            - self.__ball_radius * self.__shrink_length / 2.0,
            self.__ball_radius * self.__shrink_width,
            self.__ball_radius * self.__shrink_length,
        )
        ball_around = QRectF(
            self.__observer.ball.y * self.__shrink_width + self.__field_center.x() - 13,
            self.__observer.ball.x * self.__shrink_length + self.__field_center.y() - 13,
            26,
            26,
        )
        self.__ui.drawArc(ball_around, 0, 180 * 16)
        self.__ui.drawArc(ball_around, 0, 360 * 16)

        self.__ui.setPen(QColor("black"))
        self.__ui.setBrush(QColor("orange"))
        self.__ui.drawArc(ball_center, 0, 180 * 16)
        self.__ui.drawArc(ball_center, 0, 360 * 16)
