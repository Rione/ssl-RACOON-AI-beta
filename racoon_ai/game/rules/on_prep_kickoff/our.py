#!/usr/bin/env python3.10

"""our.py

    This module contains:
        - on_prep_kickoff_our_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_prep_kickoff_our_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_kickoff_our_cbf

    This function is for prepare our kickoff.

    Args:
        logger (Logger): Logger instance
        strategy (Strategy): Strategy instance
    Returns:
        list[RobotCommand]
    """
    strategy.defense.default_position()

    strategy.keeper.main()

    strategy.out_of_play.pre_kick_off_offense(True)

    send_cmds: list[RobotCommand] = []
    send_cmds += strategy.defense.send_cmds
    send_cmds += strategy.keeper.send_cmds
    send_cmds += strategy.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
