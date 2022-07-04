#!/usr/bin/env python3.10

"""on_halt.py

    This module contains:
        - on_halt_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.movement import halt_all
from racoon_ai.observer import Observer


def on_halt_cbf(logger: Logger, observer: Observer) -> list[RobotCommand]:
    """on_halt_cbf

    This function is called when the game is halted.
    """
    send_cmds: list[RobotCommand] = halt_all(observer.target_ids, observer.is_real)
    logger.debug(send_cmds)
    return send_cmds
