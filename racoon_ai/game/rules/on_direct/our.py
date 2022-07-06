#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_direct_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense

from ..on_stop import on_stop_cbf


def on_direct_our_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_direct_our_cbf

    This function is called at our direct free kick.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): Tuple of strategy instances.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds
