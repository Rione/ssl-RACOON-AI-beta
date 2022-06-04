#!/usr/bin/env python3.10
# flake8: ignore-errors
# pylint: disable-all
# type: ignore
"""view.py

    This module is for the Gui class.
"""
from racoon_ai.gui.background import Back
from racoon_ai.gui.chart import Chart
from racoon_ai.gui.game_control import Game
from racoon_ai.gui.main import Main
from racoon_ai.gui.robot import Robot
from racoon_ai.gui.vision import Vision
from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Gui:
    def __init__(self, is_gui_view: bool, observer: MWReceiver, role: Role):
        self.__is_gui_view = is_gui_view
        if self.__is_gui_view:
            self.__main = Main(observer, role)
            _ = Vision(self.__main)
            _ = Robot(self.__main)
            _ = Back(self.__main)
            _ = Chart(self.__main, observer)
            _ = Game(self.__main)
            self.__main.show()

    def update(self) -> None:
        if self.__is_gui_view:
            self.__main.update()
