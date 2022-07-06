#!/usr/bin/env python3.10

"""their.py

    This module contains:
        - on_prep_penalty_their_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

from ..on_stop import on_stop_cbf


def on_prep_penalty_their_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_penalty_their_cbf

    This function is to prepare enemy penalty.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, strategy)
    logger.debug(send_cmds)
    return send_cmds
