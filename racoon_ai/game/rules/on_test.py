#!/usr/bin/env python3.10

"""on_test.py

    This module contains:
        - test_cbf
"""

from logging import Logger

from racoon_ai.models.robot import RobotCommand
from racoon_ai.strategy import Strategy

# from .on_halt import on_halt_cbf
# from .on_placement import on_placement_our_cbf
# from .on_normal_start import on_default_cbf
from .on_stop import on_stop_cbf

# from .on_prep_kickoff import on_prep_kickoff_our_cbf


def test_cbf(logger: Logger, args: Strategy) -> list[RobotCommand]:
    """on_default_cbf

    This function is called when the game is running normally.

    Args:
        logger (Logger): Logger instance.
        args: (Strategy) instance.
    """

    args.keeper.main()
    args.defense.default_position()

    send_cmds: list[RobotCommand] = []
    send_cmds += on_stop_cbf(logger, args)
    # send_cmds += on_default_cbf(logger, args)
    # send_cmds += on_placement_our_cbf(logger, args)
    # send_cmds += on_prep_kickoff_our_cbf(logger, args)

    # send_cmds += args.keeper.send_cmds
    # send_cmds += args.defense.send_cmds
    # send_cmds += args.offense.send_cmds
    # send_cmds += args.out_of_play.send_cmds

    logger.debug(send_cmds)
    return send_cmds
