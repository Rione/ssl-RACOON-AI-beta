#!/usr/bin/env python 3.10
# pylint: disable=C0114

from configparser import ConfigParser
from logging import Logger

from .command_sender import CommandSender


def create_sender(
    config: ConfigParser,
    logger: Logger,
    target_ids: set[int],
    is_real: bool = False,
    is_team_yellow: bool = False,
) -> CommandSender:
    """create_sender

    This function is for creating a CommandSender.

    Returns:
        CommandSender
    """
    if (is_real) or not config.getboolean("command_sender", "use_custom_addr", fallback=False):
        return CommandSender(target_ids, is_real, is_team_yellow)
    target_host: str = config.get("command_sender", "host") or "localhost"
    target_port: int = int(config.get("command_sender", "port") or 20011)
    logger.info("Using custom address for target: %s:%d", target_host, target_port)
    return CommandSender(target_ids, is_team_yellow=is_team_yellow, host=target_host, port=target_port)


__all__ = [
    "CommandSender",
    "create_sender",
]
