#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from configparser import ConfigParser
from logging import Logger, shutdown

from .gui import Gui
from .models.robot import SimCommands
from .movement import Controls, create_controls
from .networks.sender import CommandSender, create_sender
from .observer import Observer, create_observer
from .strategy import Keeper, Offense, Role, SubRole


def main(conf: ConfigParser, logger: Logger) -> None:
    """main

    This function is for the main function.

    Returns:
        None
    """
    with_gui_view: bool = False  # Flag if view gui

    try:
        observer: Observer = create_observer(conf, logger)

        controls: Controls = create_controls(conf, logger, observer)

        role: Role = Role(observer)

        gui = Gui(with_gui_view, observer, role)

        subrole: SubRole = SubRole(observer, role)

        offense: Offense = Offense(observer)

        keeper: Keeper = Keeper(observer, role, controls)

        sender: CommandSender = create_sender(
            conf,
            logger,
            observer.target_ids,
            observer.is_real,
            observer.is_team_yellow,
        )

        logger.info("Roop started")

        while True:
            # Create a list of commands (Timestamp is set at this initialization)
            sim_cmds = SimCommands(observer.is_team_yellow)

            # Recieve commands from the MW
            observer.main()
            role.main()
            subrole.main()

            keeper.main()
            # offense.main()

            # update gui
            gui.update()

            sim_cmds.robot_commands += keeper.send_cmds
            sim_cmds.robot_commands += offense.send_cmds
            sender.send(sim_cmds)

            # update gui
            gui.update()

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)
        del gui

    finally:
        logger.info("Cleaning up...")
        shutdown()


if __name__ == "__main__":
    from logging import INFO, Formatter, StreamHandler, getLogger

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

    main(parser, log)
