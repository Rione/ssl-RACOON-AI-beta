#!/usr/bin/env python3.10
# pylint: disable=C0111

from logging import Logger
from typing import Callable, TypeAlias

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer
from racoon_ai.strategy import StrategyBase

from .on_default import on_default_cbf
from .on_halt import on_halt_cbf

RULE_ARG_TYPE: TypeAlias = tuple[StrategyBase, ...] | Observer


def rule_handler(
    func: Callable[[Logger, RULE_ARG_TYPE], list[RobotCommand]],
    logger: Logger,
    args: RULE_ARG_TYPE,
) -> list[RobotCommand]:
    """rule_handler

    This function is called when the game is running normally.

    Args:
        func (Callable[[Logger, RULE_ARG_TYPE], list[RobotCommand]]): Callback function.
        logger (Logger): Logger instance.
        args RULE_ARG_TYPE: arguments for the callback function.
    """
    logger.debug("rule_handler: %s(%s)", func, args)
    return func(logger, args)


__all__ = [
    "RULE_ARG_TYPE",
    "rule_handler",
    "on_default_cbf",
    "on_halt_cbf",
]
