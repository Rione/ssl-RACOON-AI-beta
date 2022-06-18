#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all

"""view.py

    This module is for the Gui class.
"""

from PyQt6.QtWidgets import QApplication

from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role

from .background import Back
from .chart import Chart
from .game_control import Game
from .main import Main
from .robot import Robot
from .vision import Vision


class Gui:
    def __init__(self, argv: list[str], is_gui_view: bool, observer: MWReceiver, role: Role):
        self.__app = QApplication(argv)
        self.__is_gui_view = is_gui_view
        if self.__is_gui_view:
            self.__main = Main(observer, role)
            self.__chart = Chart(self.__main, observer)
            Vision(self.__main)
            Robot(self.__main)
            Back(self.__main)
            Game(self.__main)

            self.__main.show()

    def update(self) -> None:
        if self.__is_gui_view:
            self.__main.update()
            self.__app.processEvents()
