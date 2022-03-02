#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import InitVar, dataclass
from logging import getLogger
from typing import Optional

BUFFSIZE: int = 2048


@dataclass(frozen=True)
class IPNetAddr:
    """IPNetAddr

    Attributes:
        host (str): The distination IP or hostname
        port (int): The distination port
    """

    host: str
    port: int
    mod_name: InitVar[Optional[str]] = None

    def __post_init__(self, mod_name: Optional[str]) -> None:
        if mod_name:
            getLogger(mod_name).info("Using %s:%d", self.host, self.port)
        else:
            getLogger(type(self).__module__).info("Using %s:%d", self.host, self.port)
