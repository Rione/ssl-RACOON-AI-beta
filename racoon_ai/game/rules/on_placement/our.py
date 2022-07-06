#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_placement_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import OutOfPlay


def on_placement_our_cbf(logger: Logger, args: tuple[OutOfPlay]) -> list[RobotCommand]:
    """on_placement_our_cbf

    This function is called at our placement.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): StrategyBase instances.

    Returns:
        list[RobotCommand]
    """
    # OutOfPlay instance
    args[0].placement()

    send_cmds: list[RobotCommand] = []
    send_cmds += args[0].send_cmds
    logger.debug(send_cmds)
    return send_cmds
