#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from logging import INFO, Formatter, StreamHandler, getLogger, shutdown

from .common.controls import Controls
from .models.robot import SimCommands
from .networks.receiver import MWReceiver
from .networks.sender import CommandSender

# from .strategy.offense import Offense
# from .strategy.role import Role
from .strategy.goal_keeper import Keeper


def main() -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """

    # Settings for logger
    fmt = Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    hdlr = StreamHandler()
    hdlr.setFormatter(fmt)
    logger = getLogger("racoon_ai")
    logger.setLevel(INFO)
    logger.addHandler(hdlr)
    logger.debug("Logger initialized")

    # List of online robot ids
    online_ids: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    # Flag if run for a real robot
    is_real: bool = False

    # Flag if our team is yellow
    is_team_yellow: bool = False

    try:

        observer = MWReceiver(host="127.0.0.1", port=30011)
        # role = Role(observer)

        controls = Controls(observer)

        # offense = Offense(observer)

        keeper = Keeper(observer, controls)

        sender = CommandSender(is_real, online_ids, host="localhost", port=20025)

        logger.info("Roop started")

        while True:
            # Create a list of commands
            sim_cmds = SimCommands(is_team_yellow)

            observer.main()
            # role.main()
            # offense.main()
            keeper.main()

            # sim_cmds.robot_commands += offense.send_cmds
            sim_cmds.robot_commands += keeper.send_cmds
            sender.send(sim_cmds)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)

    finally:
        logger.info("Cleaning up...")
        del sender
        shutdown()


if __name__ == "__main__":
    main()
