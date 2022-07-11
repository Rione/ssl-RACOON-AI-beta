#!/usr/bin/env python3.10

"""on_normal_start.py

    This module contains:
        - on_default_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

from .on_prep_kickoff import on_prep_kickoff_their_cbf


def on_default_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """

    strategy.defense.main()

    strategy.keeper.main()

    strategy.offense.main()

    send_cmds: list[RobotCommand] = []
    send_cmds += strategy.defense.send_cmds
    send_cmds += strategy.keeper.send_cmds
    send_cmds += strategy.offense.send_cmds
    logger.debug(send_cmds)

    return send_cmds


def on_kickoff_our_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_kick_our_cbf

    This function is called on our kickoff.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_default_cbf(logger, strategy)
    logger.debug(send_cmds)
    return send_cmds


def on_kickoff_their_cbf(logger: Logger, strategy: Strategy) -> list[RobotCommand]:
    """on_kick_their_cbf

    This function is called on enemy kickoff.

    Args:
        logger (Logger): Logger instance.
        strategy (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_prep_kickoff_their_cbf(logger, strategy)
    logger.debug(send_cmds)
    return send_cmds


def on_penalty_our_cbf(logger: Logger, strategies: Strategy) -> list[RobotCommand]:
    """on_penalty_our_cbf

    This function is called on our penalty.

    Args:
        logger (Logger): Logger instance.
        strategies (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """

    strategies.offense.penalty_kick(True)

    strategies.out_of_play.penalty_kick(True)

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies.offense.send_cmds
    send_cmds += strategies.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds


def on_penalty_their_cbf(logger: Logger, strategies: Strategy) -> list[RobotCommand]:
    """on_penalty_their_cbf

    This function is called on enemy penalty.

    Args:
        logger (Logger): Logger instance.
        strategies (Strategy): Strategy instance.

    Returns:
        list[RobotCommand]
    """

    strategies.keeper.main()

    strategies.out_of_play.penalty_kick(True)

    send_cmds: list[RobotCommand] = []
    send_cmds += strategies.keeper.send_cmds
    send_cmds += strategies.out_of_play.send_cmds
    logger.debug(send_cmds)
    return send_cmds
