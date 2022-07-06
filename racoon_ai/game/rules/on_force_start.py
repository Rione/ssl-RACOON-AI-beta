#!/usr/bin/env python3.10

"""on_force_start.py

    This module contains:
        - on_force_start_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

from .on_normal_start import on_default_cbf


def on_force_start_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_force_start_cbf

    This function is called when force start.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.
    """
    send_cmds: list[RobotCommand] = on_default_cbf(logger, strategy)
    logger.debug(send_cmds)
    return send_cmds
