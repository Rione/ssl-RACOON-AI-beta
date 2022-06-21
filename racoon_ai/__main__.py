#!/usr/bin/env python3.10
# pylint: disable-all
"""
    This is the main script.
"""
import signal

from configparser import ConfigParser
from logging import Logger, shutdown

from .gui import Gui
from .models.robot import SimCommands
from .movement import Controls, create_controls
from .networks.receiver import MWReceiver, create_receiver
from .networks.sender import CommandSender, create_sender
from .strategy import Keeper, Role

# Enable gui keyboard interrupt
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main(argv: list[str], conf: ConfigParser, logger: Logger) -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """
    # List of target robot ids
    target_ids: list[int] = [int(i) for i in conf.get("commons", "onlineIds", fallback="").split(",")]
    logger.info("Target robot ids: %s", target_ids)

    # Flag if run for a real robot
    is_real: bool = conf.getboolean("commons", "isReal", fallback=False)
    logger.info("Mode: %s", ("Real" if is_real else "Simulation"))

    # Flag if our team is yellow
    is_team_yellow: bool = conf.getboolean("commons", "isTeamYellow", fallback=False)
    logger.info("Team: %s", ("Yellow" if is_team_yellow else "Blue"))

    # Flag if view gui
    is_gui_view: bool = True

    try:
        observer: MWReceiver = create_receiver(conf, logger, target_ids, is_team_yellow)

        controls: Controls = create_controls(conf, logger, observer)

        role: Role = Role(observer)

        gui = Gui(argv, is_gui_view, observer, role)

        # offense: Offense = Offense(observer)

        keeper: Keeper = Keeper(observer, role, controls)

        sender: CommandSender = create_sender(conf, logger, target_ids, is_real)

        logger.info("Roop started")
        while True:
            # Create a list of commands (Timestamp is set at this initialization)
            sim_cmds = SimCommands(observer.is_team_yellow)

            # Recieve commands from the MW
            observer.main()
            role.main()

            # offense.main()
            keeper.main()

            # sim_cmds.robot_commands += offense.send_cmds
            sim_cmds.robot_commands += keeper.send_cmds
            sender.send(sim_cmds)

            # update gui
            gui.update()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)

    finally:
        logger.info("Cleaning up...")
        shutdown()


if __name__ == "__main__":
    from logging import INFO, Formatter, StreamHandler, getLogger
    from sys import argv

    from . import __version__

    logo: str = """
        ######     ###      ####    #####    #####   ##   ##             ###     ######
        ##  ##   ## ##    ##  ##  ### ###  ### ###  ###  ##            ## ##      ##
        ##  ##  ##   ##  ##       ##   ##  ##   ##  #### ##           ##   ##    ##
        #####   ##   ##  ##       ##   ##  ##   ##  #######           ##   ##    ##
        ## ##   #######  ##       ##   ##  ##   ##  ## ####           #######    ##
        ## ##   ##   ##   ##  ##  ### ###  ### ###  ##  ###           ##   ##     ##
        ### ###  ##   ##    ####    #####    #####   ##   ##           ##   ##   ######
    """
    print(logo)

    # Settings for logger
    fmt = Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    hdlr = StreamHandler()
    hdlr.setFormatter(fmt)
    log = getLogger("racoon_ai")
    log.setLevel(INFO)
    log.addHandler(hdlr)
    log.debug("Logger initialized")
    log.info("Running v%s", __version__)

    parser = ConfigParser()
    parser.read("racoon_ai/config.ini")

    main(argv, parser, log)
