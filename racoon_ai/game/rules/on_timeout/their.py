#!/usr/bin/env python3.10

"""their.py

    This module contains:
        - on_timeout_their_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer

from ..on_stop import on_stop_cbf


def on_timeout_their_cbf(logger: Logger, observer: Observer) -> list[RobotCommand]:
    """on_timeout_their_cbf

    This function is to prepare enemy timeout.

    Args:
        logger (Logger): Logger instance.
        observer (Observer): Observer instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, observer)
    logger.debug(send_cmds)
    return send_cmds
