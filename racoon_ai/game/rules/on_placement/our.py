#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_placement_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import BallPlacement


def on_placement_our_cbf(logger: Logger, args: tuple[BallPlacement]) -> list[RobotCommand]:
    """on_placement_our_cbf

    This function is called at our placement.

    Args:
        logger (Logger): Logger instance.
        observer (Observer): Observer instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand]
    send_cmds = [args[0].main()]
    logger.debug(send_cmds)
    return send_cmds
