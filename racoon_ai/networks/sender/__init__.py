#!/usr/bin/env python 3.10
# pylint: disable=C0114

from configparser import ConfigParser
from logging import Logger

from racoon_ai.observer import Observer

from .command_sender import CommandSender


def create_sender(config: ConfigParser, logger: Logger, observer: Observer) -> CommandSender:
    """create_sender

    This function is for creating a CommandSender.

    Returns:
        CommandSender
    """
    if (observer.is_real) and not config.getboolean("command_sender", "use_custom_addr", fallback=False):
        return CommandSender(observer)
    target_host: str = config.get("command_sender", "host") or "localhost"
    target_port: int = int(config.get("command_sender", "port") or 20011)
    logger.info("Using custom address for target: %s:%d", target_host, target_port)
    return CommandSender(observer, host=target_host, port=target_port)


__all__ = [
    "CommandSender",
    "create_sender",
]
