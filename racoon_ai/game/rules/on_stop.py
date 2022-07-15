#!/usr/bin/env python3.10

"""on_stop.py

    This module contains:
        - on_stop_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy


def on_stop_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.
    """
    # strategy.defense.main()

    # strategy.keeper.main()

    # strategy.stop_countup()

    strategy.out_of_play.reset_imu(without_attacker=True)

    # strategy.offense.stop_offense()
    strategy.offense.stop_attacker()

    send_cmds: list[RobotCommand] = []
    # send_cmds += strategy.defense.send_cmds
    # send_cmds += strategy.keeper.send_cmds
    send_cmds += strategy.offense.send_cmds
    send_cmds += strategy.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
