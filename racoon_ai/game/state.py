#!/usr/bin/env python3.10

from time import sleep
from typing import TypeAlias

from transitions import Machine

from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Referee_Info

if __name__ == "__main__":
    CMD: TypeAlias = Referee_Info.Command

    trans = [
        # ['start', CMD.HALT, CMD.NORMAL_START],
        ['halt', '*', CMD.HALT]
    ]

    machine = Machine(
        states=CMD.keys(),
        transitions=trans,
        initial=CMD.HALT,
        # ordered_transitions=True,
        # ignore_invalid_triggers=True,
        auto_transitions=True,
        # auto_transitions=False,
        name="racoon_ai",
    )
    while True:
        sleep(5)
        print(machine)
