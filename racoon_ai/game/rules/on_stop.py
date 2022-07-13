#!/usr/bin/env python3.10

"""on_stop.py

    This module contains:
        - on_stop_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_stop_cbf(logger: Logger, strategies: Strategy) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.

    Args:
        logger (Logger): Logger instance.
        args (Strategy): Strategy instance.
    """
    # strategies.defense.main()

    # strategies.keeper.main()

    # strategies.offense.stop_attacker()
    strategies.offense.stop_attacker()

    strategies.out_of_play.reset_imu(without_attacker=True)

    send_cmds: list[RobotCommand] = []
    # send_cmds += strategies.defense.send_cmds
    # send_cmds += strategies.keeper.send_cmds
    send_cmds += strategies.offense.send_cmds
    send_cmds += strategies.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
