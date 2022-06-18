#!/usr/bin/env python3.10
# pylint: disable-all

"""background.py

    This module is for the Back class.
"""

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

from .main import Main


class Back:
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        self.__main: Main = main
        self.__ai_text: QLabel
        self._set_text()

    def _set_text(self) -> None:
        self.__ai_text = QLabel("RACOON-AI", self.__main)
        self.__ai_text.setGeometry(0, 0, 150, 50)
        self.__ai_text.setFont(QFont("Arial", 16))
        self.__ai_text.setStyleSheet("background-color: white")
        self.__ai_text.setStyleSheet("QLabel { color : white; }")
        self.__ai_text.move(50, -5)
