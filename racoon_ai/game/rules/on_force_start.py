#!/usr/bin/env python3.10

"""on_force_start.py

    This module contains:
        - on_force_start_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Defense, Keeper, Offense

from .on_normal_start import on_default_cbf


def on_force_start_cbf(logger: Logger, strategies: tuple[Defense, Keeper, Offense]) -> list[RobotCommand]:
    """on_force_start_cbf

    This function is called when force start.
    """
    send_cmds: list[RobotCommand] = on_default_cbf(logger, strategies)
    logger.debug(send_cmds)
    return send_cmds
