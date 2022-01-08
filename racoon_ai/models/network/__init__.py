#!/usr/bin/env python3.10
# pylint: disable=C0114

from dataclasses import dataclass, field

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

    multicast_group: str = field(default="127.0.0.1", kw_only=True)

    local_address: str = field(default="0.0.0.0", kw_only=True)
