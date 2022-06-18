#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""background.py

    This module is for the Back class.
"""

from PyQt6 import QtGui
from PyQt6.QtWidgets import QLabel

from racoon_ai.gui.main import Main


class Back:
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        super(Back, self).__init__()

        self.__main = main
        self._set_text()

    def _set_text(self) -> None:
        self.__ai_text = QLabel("RACOON-AI", self.__main)
        self.__ai_text.setGeometry(0, 0, 150, 50)
        self.__ai_text.setFont(QtGui.QFont("Arial", 16))
        self.__ai_text.setStyleSheet("background-color: white")
        self.__ai_text.setStyleSheet("QLabel { color : white; }")
        self.__ai_text.move(50, -5)
