#!/usr/bin/env python3.10

"""on_stop.py

    This module contains:
        - on_stop_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense


def on_stop_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.
    """
    # Defense
    strategies[0].main()

    # Keeper
    strategies[1].main()

    # Offense
    strategies[2].stop_offense()

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies[0].send_cmds
    send_cmds += strategies[1].send_cmds
    send_cmds += strategies[2].send_cmds
    logger.debug(send_cmds)
    return send_cmds
