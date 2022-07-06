#!/usr/bin/env python3.10
# pylint: disable=C0111

from logging import Logger
from typing import Callable, Optional, TypeAlias

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer
from racoon_ai.strategy import Strategy

from . import (
    on_direct,
    on_force_start,
    on_halt,
    on_indirect,
    on_normal_start,
    on_placement,
    on_prep_kickoff,
    on_prep_penalty,
    on_stop,
    on_test,
    on_timeout,
)

RULE_ARG_TYPE: TypeAlias = Optional[Strategy | Observer]


def rule_handler(
    func: Callable[[Logger, RULE_ARG_TYPE], list[RobotCommand]],
    logger: Logger,
    args: RULE_ARG_TYPE = None,
) -> list[RobotCommand]:
    """rule_handler

    This function is called when the game is running normally.

    Args:
        func (Callable[[Logger, RULE_ARG_TYPE], list[RobotCommand]]): Callback function.
        logger (Logger): Logger instance.
        args (RULE_ARG_TYPE): arguments for the callback function.
    """
    logger.debug("rule_handler: %s(%s)", func, args)
    return func(logger, args)


__all__ = [
    "RULE_ARG_TYPE",
    "rule_handler",
    "on_direct",
    "on_force_start",
    "on_halt",
    "on_indirect",
    "on_normal_start",
    "on_placement",
    "on_prep_kickoff",
    "on_prep_penalty",
    "on_stop",
    "on_test",
    "on_timeout",
]
