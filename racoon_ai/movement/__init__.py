#!/usr/bin/env python3.10
# pylint: disable=C0114

from configparser import ConfigParser
from logging import Logger
from typing import Tuple

from racoon_ai.networks.receiver.mw_receiver import MWReceiver

from .controls import Controls


def create_controls(config: ConfigParser, logger: Logger, observer: MWReceiver) -> Controls:
    """create_controls"""
    if not config.getboolean("pid_gains", "use_custom_gains", fallback=False):
        return Controls(observer)

    kp: float = float(config.get("pid_gains", "kp") or 1)
    ki: float = float(config.get("pid_gains", "ki") or 0)
    kd: float = float(config.get("pid_gains", "kd") or 0)
    custom_gains: Tuple[float, float, float] = (kp, kd, ki)
    logger.info("Using custom PID gains (kp, kd, ki): %s", custom_gains)
    return Controls(observer, k_gain=custom_gains)


__all__ = [
    "Controls",
    "create_controls",
]
