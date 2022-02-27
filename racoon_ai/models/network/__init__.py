#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import InitVar, dataclass, field
from logging import getLogger
from typing import Optional

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
    mod_name: InitVar[Optional[str]] = None

    def __post_init__(self, mod_name: Optional[str]) -> None:
        if mod_name:
            getLogger(mod_name).info("Initializing on %s:%d", self.address, self.port)
        else:
            getLogger(type(self).__module__).info("Initializing on %s:%d", self.address, self.port)
