#!/usr/bin/env python3.10

"""background.py

    This module is for the Back class.
"""

from PySide6.QtGui import QFont  # pylint: disable=E0611
from PySide6.QtWidgets import QLabel  # pylint: disable=E0611

from .main import Main


class Back:  # pylint: disable=R0903
    """Robot
    Args:
        None
    Attributes:
        None
    """

    def __init__(self, main: Main) -> None:
        self.__main: Main = main
        self.__ai_text: QLabel
        self.__set_text()

    def __set_text(self) -> None:
        self.__ai_text = QLabel("RACOON-AI", self.__main)
        self.__ai_text.setGeometry(0, 0, 150, 50)
        self.__ai_text.setFont(QFont("Arial", 16))
        self.__ai_text.setStyleSheet("background-color: white")
        self.__ai_text.setStyleSheet("QLabel { color : white; }")
        self.__ai_text.move(50, -5)
