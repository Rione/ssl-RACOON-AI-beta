#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from configparser import ConfigParser
from logging import INFO, Formatter, Logger, StreamHandler, getLogger, shutdown
from subprocess import Popen
from typing import Callable, Optional

from .gui import Gui
from .models.robot import SimCommands
from .movement import Controls, create_controls
from .networks.sender import CommandSender, create_sender
from .observer import Observer, create_observer
from .strategy import Defense, Keeper, Role, SubRole  # Offense


class RacoonMain:
    """RacoonMain

    Args:
        conf: ConfigParser
        logger: Logger
    """

    def __init__(self, conf: ConfigParser, logger: Logger, with_mw: bool = True) -> None:

        self.__conf: ConfigParser = conf

        self.__logger: Logger = logger

        self.__racoon_mw: Optional[Popen[bytes]] = self.exec_mw() if with_mw else None

        self.__observer: Observer

        self.__controls: Controls

        self.__role: Role

        self.__gui: Gui

        self.__subrole: SubRole

        # self.__offense: Offense

        self.__keeper: Keeper

        self.__sender: CommandSender

        self.__init_mods()

    def __del__(self) -> None:
        """exit"""
        self.__kill_mw()
        shutdown()
        del self.__conf
        del self.__racoon_mw
        del self.__observer
        del self.__controls
        del self.__role
        del self.__gui
        del self.__subrole
        # del self.__offense
        del self.__keeper
        del self.__sender

    def main(self) -> None:
        """main

        This function is for the main function.

        Returns:
            None
        """
        self.__logger.info("Roop started")

        while True:
            # Create a list of commands (Timestamp is set at this initialization)
            sim_cmds = SimCommands(self.__observer.is_team_yellow)

            # Recieve commands from the MW
            self.__observer.main()
            self.__role.main()
            self.__subrole.main()

            self.__keeper.main()
            # self.__offense.main()
            self.__defense.main()

            # update gui
            self.__gui.update()

            sim_cmds.robot_commands += self.__keeper.send_cmds
            # sim_cmds.robot_commands += self.__offense.send_cmds
            sim_cmds.robot_commands += self.__defense.send_cmds
            self.__sender.send(sim_cmds)

            # update gui
            self.__gui.update()

    def exec_mw(self) -> Popen[bytes]:
        """exec_mw"""
        self.__logger.info("Starting MW...")
        vision_host: str = self.__conf.get("racoon_mw", "vision_host") or "224.5.23.2"
        vision_port: str = self.__conf.get("racoon_mw", "vision_port") or str(10006)
        self.__logger.info("Vision host: %s, port: %s", vision_host, vision_port)

        get_sim_flag: Callable[[bool], str] = lambda is_real: "" if is_real else "-s"
        sim_flag: str = get_sim_flag(self.__conf.getboolean("commons", "isReal"))

        get_team_flag: Callable[[bool], str] = lambda is_yellow: "yellow" if is_yellow else "blue"
        team_flag: str = get_team_flag(self.__conf.getboolean("commons", "isTeamYellow"))

        cmds: str = f"bin/RACOON-MW.exe -p {vision_port:s} {sim_flag:s} -t {team_flag:s} &"
        self.__logger.info("Executing: %s", cmds)
        return Popen(cmds.split(), stdin=None)

    def __kill_mw(self) -> None:
        if self.__racoon_mw:
            self.__logger.info("Killing MW...")
            self.__racoon_mw.kill()

    def __init_mods(self) -> None:
        try:
            self.__observer = create_observer(self.__conf, self.__logger)

            self.__controls = create_controls(self.__conf, self.__logger, self.__observer)

            self.__role = Role(self.__observer)

            self.__gui = Gui(self.__conf.getboolean("commons", "showGui"), self.__observer, self.__role)

            self.__subrole = SubRole(self.__observer, self.__role)

            # self.__offense = Offense(self.__observer, self.__role, self.__subrole, self.__controls)

            self.__defense = Defense(self.__observer, self.__role, self.__subrole, self.__controls)

            self.__keeper = Keeper(self.__observer, self.__role, self.__controls)

            self.__sender = create_sender(
                self.__conf,
                self.__logger,
                self.__observer.target_ids,
                self.__observer.is_real,
                self.__observer.is_team_yellow,
            )

        except Exception as err:  # pylint: disable=W0703
            self.__logger.error("Error while initializing\n %s", err, exc_info=True)
            self.__kill_mw()
            shutdown()


if __name__ == "__main__":
    from sys import exit as sys_exit

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

    racoon: RacoonMain = RacoonMain(parser, log, parser.getboolean("commons", "withMW"))
    racoon.main()
    sys_exit(0)
