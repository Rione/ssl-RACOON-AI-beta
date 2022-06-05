#!/usr/bin/env python3.10

"""gui.py

    This is the gui script.
"""
import sys

from PyQt5.QtWidgets import QApplication

from racoon_ai.gui.main import Gui


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None`
    """
    app = QApplication(sys.argv)
    _ = Gui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
