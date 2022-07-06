#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_placement_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_placement_our_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_placement_our_cbf

    This function is called at our placement.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    # OutOfPlay instance
    strategy.out_of_play.placement_our()

    send_cmds: list[RobotCommand] = []
    send_cmds += strategy.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
