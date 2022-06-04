#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""game_control.py

    This module is for the Game class.
"""
import math

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QSpinBox, QVBoxLayout, QWidget
from qtwidgets import AnimatedToggle, Toggle

from racoon_ai.networks.receiver import MWReceiver


class Game(QWidget, QPainter):
    """Game
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, observer: MWReceiver) -> None:
        super(Game, self).__init__()
        self.__ui: QPainter()
        self.__observer: MWReceiver = observer

        self._set_texts()

        combo = QComboBox(self)
        combo.addItem("NORMAL_START")
        combo.addItem("STOP")
        combo.resize(150, 140)
        combo.move(1205, 70)

        replace_x = QSpinBox(self)
        replace_x.resize(70, 30)
        replace_x.setMaximum(6000)
        replace_x.setMinimum(-6000)
        replace_x.move(1230, 175)
        replace_y = QSpinBox(self)
        replace_y.resize(70, 30)
        replace_y.setMaximum(60000)
        replace_y.setMinimum(-6000)
        replace_y.move(1230, 200)

        score_blue = QSpinBox(self)
        score_blue.resize(90, 30)
        score_blue.setMaximum(6000)
        score_blue.setMinimum(-6000)
        score_blue.move(1230, 300)
        score_yellow = QSpinBox(self)
        score_yellow.resize(90, 30)
        score_yellow.setMaximum(60000)
        score_yellow.setMinimum(-6000)
        score_yellow.move(1230, 328)

        button = QPushButton("Send Replacement !", self)
        button.resize(240, 32)
        button.move(1147, 232)

    def paintEvent(self, event) -> None:
        self.__ui = QPainter(self)

        self.__ui.setBrush(QColor("#2E333A"))
        self.__ui.setPen(QColor(Qt.white))
        self.__ui.drawRect(1130, 35, 270, 355)
        self.__ui.setPen(QColor("#2E333A"))
        self.__ui.drawLine(1145, 35, 1290, 35)

        self.__ui.end()

    def _set_texts(self) -> None:
        self.__gc_text = QLabel("Game Control", self)
        self.__gc_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__gc_text.setStyleSheet("QLabel { color : white; }")
        self.__gc_text.move(1150, 22)

        self.__local_text = QLabel("Local:", self)
        self.__local_text.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__local_text.setStyleSheet("QLabel { color : white; }")
        self.__local_text.move(1145, 58)

        self.__command_text = QLabel("Cmd :", self)
        self.__command_text.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__command_text.setStyleSheet("QLabel { color : white; }")
        self.__command_text.move(1147, 100)

        self.__command = QLabel("NORMAL_START", self)
        self.__command.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Black))
        self.__command.setStyleSheet("QLabel { color : white; }")
        self.__command.move(1210, 102)

        self.__replacement = QLabel("Replace", self)
        self.__replacement.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__replacement.setStyleSheet("QLabel { color : white; }")
        self.__replacement.move(1147, 155)

        self.__replacement_x = QLabel("X  :", self)
        self.__replacement_x.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__replacement_x.setStyleSheet("QLabel { color : white; }")
        self.__replacement_x.move(1195, 180)
        self.__replacement_y = QLabel("Y  :", self)
        self.__replacement_y.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__replacement_y.setStyleSheet("QLabel { color : white; }")
        self.__replacement_y.move(1195, 205)
        self.__mm_x = QLabel("mm", self)
        self.__mm_x.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__mm_x.setStyleSheet("QLabel { color : white; }")
        self.__mm_x.move(1315, 180)
        self.__mm_y = QLabel("mm", self)
        self.__mm_y.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__mm_y.setStyleSheet("QLabel { color : white; }")
        self.__mm_y.move(1315, 207)

        self.__score = QLabel("Score", self)
        self.__score.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__score.setStyleSheet("QLabel { color : white; }")
        self.__score.move(1147, 273)
        self.__score_blue = QLabel("Blue :", self)
        self.__score_blue.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__score_blue.setStyleSheet("QLabel { color : white; }")
        self.__score_blue.move(1175, 302)
        self.__score_yellow = QLabel("Yellow :", self)
        self.__score_yellow.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__score_yellow.setStyleSheet("QLabel { color : white; }")
        self.__score_yellow.move(1158, 329)
