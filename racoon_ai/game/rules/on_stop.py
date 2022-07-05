#!/usr/bin/env python3.10

"""on_stop.py

    This module contains:
        - on_stop_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense


def on_stop_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.

    Args:
        logger (Logger): Logger instance.
        args (tuple[Defense, Keeper, Offense]): Tuple of strategy instances.
    """
    # Defense
    args[0].main()

    # Keeper
    args[1].main()

    # Offense
    args[2].stop_offense()

    send_cmds: list[RobotCommand] = []
    send_cmds += args[0].send_cmds
    send_cmds += args[1].send_cmds
    send_cmds += args[2].send_cmds
    logger.debug(send_cmds)
    return send_cmds
