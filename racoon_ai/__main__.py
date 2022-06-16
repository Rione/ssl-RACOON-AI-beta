#!/usr/bin/env python3.10

"""
    This is the main script.
"""
from configparser import ConfigParser
from logging import INFO, Formatter, Logger, StreamHandler, getLogger, shutdown
from typing import Tuple

from .models.robot import SimCommands
from .movement import Controls
from .networks.receiver import MWReceiver
from .networks.sender import CommandSender

# from .strategy.defense import Defense
from .strategy.goal_keeper import Keeper

# from .strategy.offense import Offense
from .strategy.role import Role
from .strategy.subrole import SubRole


def main(conf: ConfigParser, logger: Logger) -> None:  # pylint: disable=R0914,R0915
    """main

    This function is for the main function.

    Returns:
        None
    """
    # List of online robot ids
    online_ids: list[int] = [int(i) for i in conf.get("commons", "onlineIds", fallback="").split(",")]
    logger.info("Online robot ids: %s", online_ids)

    num_bots: int = len(online_ids)
    logger.info("Number of robots: %d", num_bots)

    # Flag if run for a real robot
    is_real: bool = conf.getboolean("commons", "isReal", fallback=False)
    logger.info("Mode: %s", ("Real" if is_real else "Simulation"))

    # Flag if our team is yellow
    is_team_yellow: bool = conf.getboolean("commons", "isTeamYellow", fallback=False)
    logger.info("Team: %s", ("Yellow" if is_team_yellow else "Blue"))

    try:
        observer: MWReceiver
        if conf.getboolean("mw_receiver", "use_custom_addr", fallback=False):
            mw_host: str = conf.get("mw_receiver", "host") or "localhost"
            mw_port: int = int(conf.get("mw_receiver", "port") or 30011)
            logger.info("Using custom address for MW: %s:%d", mw_host, mw_port)
            observer = MWReceiver(host=mw_host, port=mw_port)
        else:
            observer = MWReceiver()

        controls: Controls
        if conf.getboolean("pid_gains", "use_custom_gains", fallback=False):
            kp: float = float(conf.get("pid_gains", "kp") or 1)
            ki: float = float(conf.get("pid_gains", "ki") or 0)
            kd: float = float(conf.get("pid_gains", "kd") or 0)
            custom_gains: Tuple[float, float, float] = (kp, kd, ki)
            logger.info("Using custom PID gains: %s", custom_gains)
            controls = Controls(observer, k_gain=custom_gains)
        else:
            controls = Controls(observer)

        role: Role = Role(observer)

        subrole: SubRole = SubRole(observer, role)

        # offense: Offense = Offense(observer)

        # defense = Defense(observer, controls)

        keeper: Keeper = Keeper(observer, role, controls)

        sender: CommandSender
        if (not is_real) and conf.getboolean("command_sender", "use_custom_addr", fallback=False):
            target_host: str = conf.get("command_sender", "host") or "localhost"
            target_port: int = int(conf.get("command_sender", "port") or 20011)
            sender = CommandSender(is_real, online_ids, host=target_host, port=target_port)
        else:
            sender = CommandSender(is_real, online_ids)

        logger.info("Roop started")

        while True:
            # Create a list of commands (Timestamp is set at this initialization)
            sim_cmds = SimCommands(is_team_yellow)

            observer.main()
            role.main()
            subrole.main()
            # offense.main()
            # defense.main()
            keeper.main()

            # sim_cmds.robot_commands += offense.send_cmds
            # sim_cmds.robot_commands += defense.send_cmds
            sim_cmds.robot_commands += keeper.send_cmds
            sender.send(sim_cmds)

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received", exc_info=False)

    finally:
        logger.info("Cleaning up...")
        shutdown()


if __name__ == "__main__":
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
