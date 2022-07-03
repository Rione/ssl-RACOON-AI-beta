#!/usr/bin/env python3.10

"""on_test.py

    This module contains:
        - test_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense

from .on_normal_start import on_default_cbf


def test_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        strategies: tuple[Defense, Keeper, Offense]
    """
    send_cmds: list[RobotCommand] = on_default_cbf(logger, strategies)
    logger.debug(send_cmds)
    return send_cmds