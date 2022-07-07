#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_prep_penalty_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

from ..on_stop import on_stop_cbf


def on_prep_penalty_our_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_penalty_our_cbf

    This function is for prepare our PK attack.

    Args:
        logger (Logger): Logger instance
        strategy (Strategy): Strategy instance
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, strategy)
    logger.debug(send_cmds)
    return send_cmds
