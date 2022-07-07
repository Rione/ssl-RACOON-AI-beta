#!/usr/bin/env python3.10
"""view.py

    This module is for the Gui class.
"""
from logging import getLogger

from PySide6.QtWidgets import QApplication  # pylint: disable=E0611

from racoon_ai.observer import Observer
from racoon_ai.strategy.role import Role

from .modules import Back, Chart, Game, Main, Robot, Vision


class Gui:  # pylint: disable=R0903
    """Gui

    Args:
        argv: list[str]
        is_gui_view: bool
        observer: Observer
        role: Role
    """

    def __init__(self, is_gui_view: bool, observer: Observer, role: Role):
        self.__logger = getLogger(__name__)
        self.__logger.debug("create logger")

        self.__app = QApplication()
        self.__is_gui_view = is_gui_view
        self.__logger.info("GUI: %s", is_gui_view)
        if self.__is_gui_view:
            self.__setup(observer, role)

    def __del__(self) -> None:
        """__del__"""
        self.__app.exit(0)

    def __setup(self, observer: Observer, role: Role) -> None:
        """setup"""
        self.__main = Main(observer, role)
        Chart(self.__main, observer)
        Vision(self.__main)
        Robot(self.__main)
        Back(self.__main)
        Game(self.__main)
        self.__main.show()

    def update(self) -> None:
        """update"""
        if not self.__is_gui_view:
            return
        self.__main.update()
        self.__app.processEvents()  # type: ignore
