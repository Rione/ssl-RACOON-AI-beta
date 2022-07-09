#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_prep_penalty_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_prep_penalty_our_cbf(logger: Logger, strategies: Strategy) -> list[RobotCommand]:
    """on_penalty_our_cbf

    This function is for prepare our PK attack.

    Args:
        logger (Logger): Logger instance
        strategies (Strategy): Strategy instance
    """
    strategies.offense.penalty_kick(True)

    strategies.out_of_play.penalty_kick(True)

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies.offense.send_cmds
    send_cmds += strategies.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
