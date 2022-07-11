#!/usr/bin/env python3.10

"""their.py

    This module contains:
        - on_direct_their_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_direct_their_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_direct_their_cbf

    This function is to prepare enemy direct free kick.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    strategy.defense.main()

    strategy.keeper.main()

    strategy.offense.direct_their()

    send_cmds: list[RobotCommand] = []
    send_cmds += strategy.defense.send_cmds
    send_cmds += strategy.keeper.send_cmds
    send_cmds += strategy.offense.send_cmds
    logger.debug(send_cmds)
    return send_cmds
