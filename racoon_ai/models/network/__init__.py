#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import dataclass, field
from logging import getLogger

BUFFSIZE: int = 2048


@dataclass()
class Network:
    """Network

    Attributes:
        port (int)
        multicast_group (str)
        local_address (str)
    """

    port: int = field()

    multicast_group: str = field(default="224.5.23.2", kw_only=True)

    local_address: str = field(default="0.0.0.0", kw_only=True)

    def __post_init__(self) -> None:
        self.__logger = getLogger(type(self).__module__)
        self.__logger.info("Initialized on %s:%d", self.multicast_group, self.port)
