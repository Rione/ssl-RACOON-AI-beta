#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_direct_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense

from ..on_normal_start import on_default_cbf


def on_direct_our_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_direct_our_cbf

    This function is called at our direct free kick.

    Args:
        logger (Logger): Logger instance.
        strategies (tuple[Defense, Keeper, Offense]): Strategies.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_default_cbf(logger, strategies)
    logger.debug(send_cmds)
    return send_cmds
