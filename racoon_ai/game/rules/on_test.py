#!/usr/bin/env python3.10

"""on_test.py

    This module contains:
        - test_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import OutOfPlay

from .on_placement import on_placement_our_cbf

# from racoon_ai.strategy import Defense, Keeper, Offense

# from .on_normal_start import on_default_cbf
# from .on_stop import on_stop_cbf


def test_cbf(logger: Logger, args: tuple[OutOfPlay]) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        args: tuple[StrategyBase, ...]
    """
    # send_cmds: list[RobotCommand] = on_default_cbf(logger, args)
    # send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    send_cmds: list[RobotCommand] = on_placement_our_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds
