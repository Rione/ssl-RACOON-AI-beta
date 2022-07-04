#!/usr/bin/env python3.10

"""on_test.py

    This module contains:
        - test_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import BallPlacement

from .on_placement import on_placement_our_cbf


def test_cbf(logger: Logger, args: tuple[BallPlacement]) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        args: tuple[BallPlacement]
    """
    send_cmds: list[RobotCommand] = on_placement_our_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds
