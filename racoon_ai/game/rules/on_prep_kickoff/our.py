#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_prep_kickoff_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

# from ..on_stop import on_stop_cbf


def on_prep_kickoff_our_cbf(logger: Logger, strategies: Strategy) -> list[RobotCommand]:
    """on_kickoff_our_cbf

    This function is for prepare our kickoff.

    Args:
        logger (Logger): Logger instance
        strategies (Strategy): Strategy instance
    Returns:
        list[RobotCommand]
    """
    strategies.defense.default_position()

    strategies.keeper.main()

    strategies.out_of_play.pre_kick_off_offense(True)

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies.defense.send_cmds
    send_cmds += strategies.keeper.send_cmds
    send_cmds += strategies.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
