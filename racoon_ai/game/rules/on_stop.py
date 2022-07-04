#!/usr/bin/env python3.10

"""on_stop.py

    This module contains:
        - on_stop_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer

from .on_halt import on_halt_cbf


def on_stop_cbf(logger: Logger, observer: Observer) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.
    """
    send_cmds: list[RobotCommand] = on_halt_cbf(logger, observer)
    logger.debug(send_cmds)
    return send_cmds
