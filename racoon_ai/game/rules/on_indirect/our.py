#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_indirect_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer

from ..on_stop import on_stop_cbf


def on_indirect_our_cbf(logger: Logger, observer: Observer) -> list[RobotCommand]:
    """on_indirect_our_cbf

    This function is called at our indirect free kick.

    Args:
        logger (Logger): Logger instance.
        observer (Observer): Observer instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, observer)
    logger.debug(send_cmds)
    return send_cmds
