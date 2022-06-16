#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""game_control.py

    This module is for the Game class.
"""
from PyQt6 import QtGui
from PyQt6.QtWidgets import QComboBox, QLabel, QPushButton, QSpinBox

from racoon_ai.gui.animated_toggle import AnimatedToggle
from racoon_ai.gui.main import Main


class Game:
    """Game
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        super(Game, self).__init__()
        self.__main = main

        self._set_texts()
        self._set_toggle()
        self._set_combo()
        self._set_box()
        self._set_button()

    def _set_texts(self) -> None:

        self.__gc_text = QLabel("Game Control", self.__main)
        self.__gc_text.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__gc_text.setStyleSheet("QLabel { color : white; }")
        self.__gc_text.move(1172, 44)

        self.__local_text = QLabel("Local:", self.__main)
        self.__local_text.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__local_text.setStyleSheet("QLabel { color : white; }")
        self.__local_text.move(1167, 80)

        self.__command_text = QLabel("Cmd :", self.__main)
        self.__command_text.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__command_text.setStyleSheet("QLabel { color : white; }")
        self.__command_text.move(1169, 122)

        self.__command = QLabel("NORMAL_START", self.__main)
        self.__command.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__command.setStyleSheet("QLabel { color : white; }")
        self.__command.move(1232, 124)

        self.__replacement = QLabel("Replace", self.__main)
        self.__replacement.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__replacement.setStyleSheet("QLabel { color : white; }")
        self.__replacement.move(1169, 177)

        self.__replacement_x = QLabel("X  :", self.__main)
        self.__replacement_x.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__replacement_x.setStyleSheet("QLabel { color : white; }")
        self.__replacement_x.move(1217, 202)
        self.__replacement_y = QLabel("Y  :", self.__main)
        self.__replacement_y.setFont(QtGui.QFont("Arial", 16, QtGui.QFont.Black))
        self.__replacement_y.setStyleSheet("QLabel { color : white; }")
        self.__replacement_y.move(1217, 227)
        self.__mm_x = QLabel("mm", self.__main)
        self.__mm_x.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__mm_x.setStyleSheet("QLabel { color : white; }")
        self.__mm_x.move(1337, 202)
        self.__mm_y = QLabel("mm", self.__main)
        self.__mm_y.setFont(QtGui.QFont("Arial", 15, QtGui.QFont.Black))
        self.__mm_y.setStyleSheet("QLabel { color : white; }")
        self.__mm_y.move(1337, 229)

        self.__score = QLabel("Score", self.__main)
        self.__score.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Black))
        self.__score.setStyleSheet("QLabel { color : white; }")
        self.__score.move(1169, 295)
        self.__score_blue = QLabel("Blue :", self.__main)
        self.__score_blue.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__score_blue.setStyleSheet("QLabel { color : white; }")
        self.__score_blue.move(1197, 324)
        self.__score_yellow = QLabel("Yellow :", self.__main)
        self.__score_yellow.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Black))
        self.__score_yellow.setStyleSheet("QLabel { color : white; }")
        self.__score_yellow.move(1180, 351)

    def _set_toggle(self) -> None:
        toggle_referee = AnimatedToggle(self.__main, checked_color="#FFB000", pulse_checked_color="#44FFB000")
        toggle_referee.resize(70, 50)
        toggle_referee.move(1222, 68)

    def _set_combo(self) -> None:
        combo = QComboBox(self.__main)
        combo.addItem("NORMAL_START")
        combo.addItem("STOP")
        combo.resize(150, 140)
        combo.move(1227, 92)

    def _set_box(self) -> None:
        replace_x = QSpinBox(self.__main)
        replace_x.resize(70, 30)
        replace_x.setMaximum(6000)
        replace_x.setMinimum(-6000)
        replace_x.move(1252, 197)
        replace_y = QSpinBox(self.__main)
        replace_y.resize(70, 30)
        replace_y.setMaximum(60000)
        replace_y.setMinimum(-6000)
        replace_y.move(1252, 222)

        score_blue = QSpinBox(self.__main)
        score_blue.resize(90, 30)
        score_blue.setMaximum(6000)
        score_blue.setMinimum(-6000)
        score_blue.move(1252, 322)
        score_yellow = QSpinBox(self.__main)
        score_yellow.resize(90, 30)
        score_yellow.setMaximum(60000)
        score_yellow.setMinimum(-6000)
        score_yellow.move(1252, 350)

    def _set_button(self) -> None:
        button = QPushButton("Send Replacement !", self.__main)
        button.resize(240, 32)
        button.move(1169, 254)
