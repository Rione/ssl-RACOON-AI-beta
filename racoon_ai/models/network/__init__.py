#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import dataclass, field
from logging import getLogger

BUFFSIZE: int = 2048


@dataclass(frozen=True)
class Network:
    """Network

    Attributes:
        port (int): The distination port
        address (str): The distination address
    """

    port: int = field()
    address: str = field(kw_only=True)

    def __post_init__(self) -> None:
        getLogger(type(self).__module__).info("Initializing on %s:%d", self.address, self.port)
