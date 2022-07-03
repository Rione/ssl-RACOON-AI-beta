#!/usr/bin/env python3.10

"""their.py

    This module contains:
        - on_prep_kickoff_their_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.observer import Observer

from ..on_stop import on_stop_cbf


def on_prep_kickoff_their_cbf(logger: Logger, args: Observer) -> list[RobotCommand]:
    """on_kickoff_their_cbf

    This function is to prepare enemy kickoff.
    """
    send_cmds: list[RobotCommand] = on_stop_cbf(logger, args)
    logger.debug(send_cmds)
    return send_cmds
