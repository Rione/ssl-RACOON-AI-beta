#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from configparser import ConfigParser
from logging import DEBUG, INFO, FileHandler, Formatter, Logger, StreamHandler, getLogger, shutdown
from subprocess import Popen
from typing import Callable, Optional

from .game import Game
from .movement import Controls, create_controls
from .networks.sender import CommandSender, create_sender
from .observer import Observer, create_observer


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

        self.__observer: Observer = create_observer(self.__conf, self.__logger)

        self.__controls: Controls = create_controls(self.__conf, self.__logger, self.__observer)

        self.__sender: CommandSender = create_sender(
            self.__conf,
            self.__logger,
            self.__observer.target_ids,
            self.__observer.is_real,
            self.__observer.is_team_yellow,
        )

        self.__game: Game = Game(
            self.__observer,
            self.__controls,
            self.__sender.send,
            show_gui=conf.getboolean("commons", "showGui"),
        )

        self.__game.main()

    def __del__(self) -> None:
        """exit"""
        self.__kill_mw()
        shutdown()
        del self.__conf
        del self.__racoon_mw
        del self.__observer
        del self.__controls
        del self.__sender
        del self.__game

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

        get_goal_flag: Callable[[bool], str] = lambda is_negative_side: "P" if is_negative_side else "N"
        goal_flag: str = get_goal_flag(self.__conf.getboolean("commons", "isOurCourtNegative"))

        cmds: str = f"bin/RACOON-MW.exe -g {goal_flag!s} -p {vision_port:s} {sim_flag:s} -t {team_flag:s} &"
        self.__logger.info("Executing: %s", cmds)
        return Popen(cmds.split(), stdin=None)

    def __kill_mw(self) -> None:
        if self.__racoon_mw:
            self.__logger.info("Killing MW...")
            self.__racoon_mw.kill()


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
    fmt = Formatter("[%(levelname)s] %(asctime)s %(pathname)s:%(lineno)d %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    log = getLogger("racoon_ai")
    log.setLevel(DEBUG)

    hdlr = StreamHandler()
    hdlr.setFormatter(fmt)
    hdlr.setLevel(INFO)
    log.addHandler(hdlr)

    hdlr_1 = FileHandler(".cache/racoon-ai.log", mode="w", delay=True)
    hdlr_1.setFormatter(fmt)
    hdlr_1.setLevel(DEBUG)
    # log.addHandler(hdlr_1)

    log.debug("Logger initialized")
    log.info("Running v%s", __version__)

    parser = ConfigParser()
    parser.read("racoon_ai/config.ini")

    racoon: RacoonMain = RacoonMain(parser, log, parser.getboolean("commons", "withMW"))
    sys_exit(0)
