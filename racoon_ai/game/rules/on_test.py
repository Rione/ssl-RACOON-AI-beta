#!/usr/bin/env python3.10

"""on_test.py

    This module contains:
        - on_test_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense


def test_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        strategies: tuple[Defense, Keeper, Offense]
    """

    # Defense
    strategies[0].main()

    # Keeper
    strategies[1].main()

    # Offense
    strategies[2].main()

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies[0].send_cmds
    send_cmds += strategies[1].send_cmds
    send_cmds += strategies[2].send_cmds
    logger.debug(send_cmds)

    return send_cmds
