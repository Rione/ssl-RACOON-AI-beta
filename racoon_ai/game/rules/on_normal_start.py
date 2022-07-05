#!/usr/bin/env python3.10

"""on_normal_start.py

    This module contains:
        - on_default_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense

from .on_stop import on_stop_cbf


def on_default_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        strategies: tuple[Defense, Keeper, Offense]

    Returns:
        list[RobotCommand]
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


def on_kickoff_our_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_kick_our_cbf

    This function is called on our kickoff.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): Tuple of strategy instances.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds


def on_kickoff_their_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_kick_their_cbf

    This function is called on enemy kickoff.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): Tuple of strategy instances.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds


def on_penalty_our_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_penalty_our_cbf

    This function is called on our penalty.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): Tuple of strategy instances.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds


def on_penalty_their_cbf(logger: Logger, args: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_penalty_their_cbf

    This function is called on enemy penalty.

    Args:
        logger (Logger): Logger instance.
        args (tuple[StrategyBase, ...]): Tuple of strategy instances.

    Returns:
        list[RobotCommand]
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds
