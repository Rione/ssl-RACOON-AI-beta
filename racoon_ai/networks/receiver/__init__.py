#!/usr/bin/env python 3.10
# pylint: disable=C0114

from configparser import ConfigParser
from logging import Logger

from .mw_receiver import MWReceiver


def create_receiver(config: ConfigParser, logger: Logger, target_ids: list[int], is_team_yellow: bool) -> MWReceiver:
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
