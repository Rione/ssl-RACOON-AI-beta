#!/usr/bin/env python3.10
# pylint: disable=C0114


from configparser import ConfigParser
from logging import Logger

from .observer import Observer


def create_observer(config: ConfigParser, logger: Logger) -> Observer:
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
    target_ids: set[int] = {int(i) for i in config.get("commons", "targetIds").split(",")}
    logger.info("Target robot ids: %s", target_ids)

    # Flag if run for a real robot
    is_real: bool = config.getboolean("commons", "isReal", fallback=False)
    logger.info("Mode: %s", ("Real" if is_real else "Simulation"))

    # List of IMU enabled robot ids
    imu_ids: set[int]
    if is_real and config.getboolean("commons", "use_imu"):
        imu_ids = {int(i) for i in config.get("commons", "imu_ids").split(",")}
        logger.info("IMU enabled robot ids: %s", imu_ids)
    else:
        imu_ids = set()
        logger.info("IMU disabled")

    # Flag if our team is yellow
    is_team_yellow: bool = config.getboolean("commons", "isTeamYellow", fallback=False)
    logger.info("Team: %s", ("Yellow" if is_team_yellow else "Blue"))

    if not config.getboolean("mw_receiver", "use_custom_addr", fallback=False):
        return Observer(target_ids, imu_ids, is_real, is_team_yellow)

    mw_host: str = config.get("mw_receiver", "host") or "localhost"
    mw_port: int = int(config.get("mw_receiver", "port") or 30011)
    logger.info("Using custom address for MW: %s:%d", mw_host, mw_port)
    return Observer(target_ids, imu_ids, is_real, is_team_yellow, host=mw_host, port=mw_port)


__all__ = [
    "create_observer",
    "Observer",
]
