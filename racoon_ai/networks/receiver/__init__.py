#!/usr/bin/env python 3.10
# pylint: disable=C0114

from configparser import ConfigParser
from logging import Logger

from .mw_receiver import MWReceiver


def create_receiver(config: ConfigParser, logger: Logger) -> MWReceiver:
    """create_receiver

    This function is for creating a MWReceiver.

    Args:
        config: ConfigParser
        logger: Logger
        target_ids: list[int]
        is_team_yellow: bool

    Returns:
        MWReceiver
    """
    # List of target robot ids
    target_ids: set[int] = {int(i) for i in config.get("commons", "targetIds", fallback="").split(",")}
    logger.info("Target robot ids: %s", target_ids)

    # Flag if run for a real robot
    is_real: bool = config.getboolean("commons", "isReal", fallback=False)
    logger.info("Mode: %s", ("Real" if is_real else "Simulation"))

    # Flag if our team is yellow
    is_team_yellow: bool = config.getboolean("commons", "isTeamYellow", fallback=False)
    logger.info("Team: %s", ("Yellow" if is_team_yellow else "Blue"))

    if not config.getboolean("mw_receiver", "use_custom_addr", fallback=False):
        return MWReceiver(target_ids, is_team_yellow)

    mw_host: str = config.get("mw_receiver", "host") or "localhost"
    mw_port: int = int(config.get("mw_receiver", "port") or 30011)
    logger.info("Using custom address for MW: %s:%d", mw_host, mw_port)
    return MWReceiver(target_ids, is_team_yellow, host=mw_host, port=mw_port)


__all__ = [
    "MWReceiver",
    "create_receiver",
]
