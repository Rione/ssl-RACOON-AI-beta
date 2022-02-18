#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import dataclass, field
from logging import getLogger
from typing import Optional

BUFFSIZE: int = 2048


@dataclass()
class Network:
    """Network

    Attributes:
        port (int)
        multicast_address (str)
        local_address (str)
    """

    port: int = field()

    multicast_address: str = field(default="224.5.23.2", kw_only=True)

    local_address: str = field(default="127.0.0.1", kw_only=True)

    def __init__(
        self, port: int, *, multicast_address: Optional[str] = None, local_address: Optional[str] = None
    ) -> None:

        self.port = port

        if multicast_address:
            self.multicast_address = multicast_address

        if local_address:
            self.local_address = local_address

        self.__post_init__()

    def __post_init__(self) -> None:
        self.__logger = getLogger(type(self).__module__)
        self.__logger.info("Initializing on %s:%d", self.multicast_address, self.port)
