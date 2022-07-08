#!/usr/bin/env python3.10

"""their.py

    This module contains:
        - on_timeout_their_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_timeout_their_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_timeout_their_cbf

    This function is to prepare enemy timeout.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = strategy.out_of_play.time_out()
    logger.debug(send_cmds)
    return send_cmds
