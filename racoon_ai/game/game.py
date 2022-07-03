#!/usr/bin/env python3.10

"""game.py

    This module contains:
        - Game
"""

from logging import Logger, getLogger
from typing import Callable

from racoon_ai.gui.view import Gui
from racoon_ai.models.referee import REF_COMMAND
from racoon_ai.models.robot import RobotCommand, SimCommands
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer
from racoon_ai.strategy import Defense, Keeper, Offense, Role, SubRole

from .rules import RULE_ARG_TYPE, rule_handler
from .rules.on_halt import on_halt_cbf
from .rules.on_normal_start import on_default_cbf
from .rules.on_prep_kickoff import on_prep_kickoff_our_cbf, on_prep_kickoff_their_cbf
from .rules.on_stop import on_stop_cbf
from .rules.on_test import test_cbf


class Game:
    """Game

    Args:
        observer (Observer): Observer instance.
        controles (Controls): Controls instance.
        send (Callable[[SimCommands], None]): Function to send SimCommands to the simulator.
        show_gui (bool, optional): Show GUI. (defauls: False)
        keeper_id (int, optional): Keeper ID. (defaults: 0)
    """

    def __init__(
        self,
        observer: Observer,
        controles: Controls,
        send: Callable[[SimCommands], None],
        *,
        show_gui: bool = False,
        keeper_id: int = 0,
    ) -> None:

        self.__logger: Logger = getLogger(__name__)
        self.__logger.debug("Initializing ...")

        self.__observer: Observer = observer

        self.__controls: Controls = controles

        self.__role: Role = Role(self.__observer, keeper_id=keeper_id)

        self.__send: Callable[[SimCommands], None] = send

        self.__gui: Gui = Gui(show_gui, self.__observer, self.__role)

        self.__subrole: SubRole = SubRole(self.__observer, self.__role)

        self.__offense: Offense = Offense(self.__observer, self.__role, self.__subrole, self.__controls)

        self.__defense: Defense = Defense(self.__observer, self.__role, self.__subrole, self.__controls)

        self.__keeper: Keeper = Keeper(self.__observer, self.__role, self.__controls)

    def main(self) -> None:
        """Main"""
        self.__logger.info("Starting main roop...")
        while True:
            self.__observer.main()
            self.__role.main()
            self.__subrole.main()
            self.__gui.update()

            args: tuple[
                Callable[[Logger, RULE_ARG_TYPE], list[RobotCommand]],
                RULE_ARG_TYPE,
            ] = self.handle_ref_command()
            sim_cmds = SimCommands(
                self.__observer.is_team_yellow,
                rule_handler(args[0], self.__logger, args[1]),
            )

            self.__logger.debug(sim_cmds)
            self.__send(sim_cmds)

    def handle_ref_command(self) -> tuple[Callable[..., list[RobotCommand]], RULE_ARG_TYPE]:
        """handle_ref_command"""
        self.__logger.debug("Current referee command: %s", self.__observer.referee.command_str)

        test_mode: bool = False
        if test_mode:
            return (test_cbf, (self.__defense, self.__keeper, self.__offense))
            # return (test_cbf, self.__observer)

        if self.__observer.referee.command is REF_COMMAND.HALT:
            return (on_halt_cbf, self.__observer)

        if self.__observer.referee.command is (REF_COMMAND.NORMAL_START or REF_COMMAND.FORCE_START):
            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_our_kickoff(self.__observer.referee.command):
            return (on_prep_kickoff_our_cbf, self.__observer)

        if self.__is_their_kickoff(self.__observer.referee.command):
            return (on_prep_kickoff_their_cbf, self.__observer)

        return (on_stop_cbf, None)

    def __is_our_kickoff(self, command: "REF_COMMAND.V") -> bool:
        """is_our_kickoff

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our kickoff.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_KICKOFF_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_KICKOFF_BLUE)
        )

    def __is_their_kickoff(self, command: "REF_COMMAND.V") -> bool:
        """is_their_kickoff

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their kickoff.
        """
        return not self.__is_our_kickoff(command)
