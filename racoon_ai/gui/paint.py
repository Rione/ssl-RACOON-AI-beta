#!/usr/bin/env python3.10
"""paint.py

    This module is for the paint function.
"""
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class Gui(QWidget):
    """Gui
    Args:
        None
    Attributes:
        None
    """

    def __init__(self) -> None:
        super(Gui, self).__init__()
        self._initui()
        self.geometry_width = 1300
        self.geometry_height = 850

    def _initui(self) -> None:
        self.resize(1000, 500)
        self.move(0, 0)
        self.setWindowTitle("RACOON-AI")
        self.show()

    def resizeEvent(self, event) -> None:
        """Gui
        Args:
            None
        Attributes:
            None
        """
        coat_width = event.size().width()
        coat_height = event.size().height()

        window_width = coat_width / 1300
        window_height = coat_height / 850

    def paintEvent(self) -> None:
        ui = QPainter(self)
