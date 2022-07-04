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
from racoon_ai.strategy import BallPlacement, Defense, Keeper, Offense, Role, SubRole

from .rules import RULE_ARG_TYPE, rule_handler
from .rules.on_direct import on_direct_our_cbf, on_direct_their_cbf
from .rules.on_force_start import on_force_start_cbf
from .rules.on_halt import on_halt_cbf
from .rules.on_indirect import on_indirect_our_cbf, on_indirect_their_cbf
from .rules.on_normal_start import (
    on_default_cbf,
    on_kickoff_our_cbf,
    on_kickoff_their_cbf,
    on_penalty_our_cbf,
    on_penalty_their_cbf,
)
from .rules.on_placement import on_placement_our_cbf, on_placement_their_cbf
from .rules.on_prep_kickoff import on_prep_kickoff_our_cbf, on_prep_kickoff_their_cbf
from .rules.on_prep_penalty import on_prep_penalty_our_cbf, on_prep_penalty_their_cbf
from .rules.on_stop import on_stop_cbf
from .rules.on_test import test_cbf
from .rules.on_timeout import on_timeout_our_cbf, on_timeout_their_cbf


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

        self.__ball_placement: BallPlacement = BallPlacement(self.__observer, self.__role, self.__controls)

        self.__tmp_ball_diff_sum: float = float(0)

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

    def handle_ref_command(  # pylint: disable=R0911,R0912
        self,
    ) -> tuple[Callable[..., list[RobotCommand]], RULE_ARG_TYPE]:
        """handle_ref_command"""
        self.__logger.debug("Current referee command: %s", self.__observer.referee.command_str)

        test_mode: bool = False
        if test_mode:
            # return (test_cbf, (self.__defense, self.__keeper, self.__offense))
            return (test_cbf, (self.__ball_placement,))
            # return (test_cbf, (self.__defense, self.__keeper, self.__offense))

        cmd: "REF_COMMAND.V" = self.__observer.referee.command
        if cmd is REF_COMMAND.HALT:
            return (on_halt_cbf, self.__observer)

        if cmd is REF_COMMAND.NORMAL_START:
            if prev_cmd := self.__observer.referee.pre_command:
                if self.__is_our_kickoff(prev_cmd):
                    return (on_kickoff_our_cbf, self.__observer)

                if self.__is_their_kickoff(prev_cmd):
                    return (on_kickoff_their_cbf, self.__observer)

                if self.__is_our_penalty(prev_cmd):
                    return (on_penalty_our_cbf, self.__observer)

                if self.__is_their_penalty(prev_cmd):
                    return (on_penalty_their_cbf, self.__observer)

            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if cmd is REF_COMMAND.FORCE_START:
            return (on_force_start_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_our_kickoff(cmd):
            return (on_prep_kickoff_our_cbf, self.__observer)

        if self.__is_their_kickoff(cmd):
            return (on_prep_kickoff_their_cbf, self.__observer)

        if self.__is_our_penalty(cmd):
            return (on_prep_penalty_our_cbf, self.__observer)

        if self.__is_their_penalty(cmd):
            return (on_prep_penalty_their_cbf, self.__observer)

        if self.__is_our_direct_free(cmd):
            if not self.__is_ball_moved():
                return (on_direct_our_cbf, (self.__defense, self.__keeper, self.__offense))
            self.__tmp_ball_diff_sum = float(0)
            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_their_direct_free(cmd):
            if not self.__is_ball_moved():
                return (on_direct_their_cbf, self.__observer)
            self.__tmp_ball_diff_sum = float(0)
            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_our_indirect_free(cmd):
            if not self.__is_ball_moved():
                return (on_indirect_our_cbf, self.__observer)
            self.__tmp_ball_diff_sum = float(0)
            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_their_indirect_free(cmd):
            if not self.__is_ball_moved():
                return (on_indirect_their_cbf, self.__observer)
            self.__tmp_ball_diff_sum = float(0)
            return (on_default_cbf, (self.__defense, self.__keeper, self.__offense))

        if self.__is_our_timeout(cmd):
            return (on_timeout_our_cbf, self.__observer)

        if self.__is_their_timeout(cmd):
            return (on_timeout_their_cbf, self.__observer)

        if cmd is (REF_COMMAND.GOAL_BLUE or REF_COMMAND.GOAL_YELLOW):
            pass

        if self.__is_our_placement(cmd):
            return (on_placement_our_cbf, self.__observer)

        if self.__is_their_placement(cmd):
            return (on_placement_their_cbf, self.__observer)

        return (on_stop_cbf, self.__observer)

    def __is_ball_moved(self, distance: float = 15e2) -> bool:
        """__is_ball_moved"""
        self.__tmp_ball_diff_sum += abs(self.__observer.ball.diff)
        return distance <= self.__tmp_ball_diff_sum

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
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_KICKOFF_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_KICKOFF_YELLOW)
        )

    def __is_our_penalty(self, command: "REF_COMMAND.V") -> bool:
        """is_our_penalty

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our penalty.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_PENALTY_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_PENALTY_BLUE)
        )

    def __is_their_penalty(self, command: "REF_COMMAND.V") -> bool:
        """is_their_penalty

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their penalty.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_PENALTY_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.PREPARE_PENALTY_YELLOW)
        )

    def __is_our_direct_free(self, command: "REF_COMMAND.V") -> bool:
        """is_our_direct_free

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our direct.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.DIRECT_FREE_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.DIRECT_FREE_BLUE)
        )

    def __is_their_direct_free(self, command: "REF_COMMAND.V") -> bool:
        """is_their_direct_free

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their direct.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.DIRECT_FREE_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.DIRECT_FREE_YELLOW)
        )

    def __is_our_indirect_free(self, command: "REF_COMMAND.V") -> bool:
        """is_our_indirect_free

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our indirect.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.INDIRECT_FREE_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.INDIRECT_FREE_BLUE)
        )

    def __is_their_indirect_free(self, command: "REF_COMMAND.V") -> bool:
        """is_their_indirect_free

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their indirect.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.INDIRECT_FREE_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.INDIRECT_FREE_YELLOW)
        )

    def __is_our_timeout(self, command: "REF_COMMAND.V") -> bool:
        """is_our_timeout

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our timeout.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.TIMEOUT_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.TIMEOUT_BLUE)
        )

    def __is_their_timeout(self, command: "REF_COMMAND.V") -> bool:
        """is_their_timeout

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their timeout.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.TIMEOUT_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.TIMEOUT_YELLOW)
        )

    def __is_our_placement(self, command: "REF_COMMAND.V") -> bool:
        """is_our_placement

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is our placement.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.BALL_PLACEMENT_YELLOW)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.BALL_PLACEMENT_BLUE)
        )

    def __is_their_placement(self, command: "REF_COMMAND.V") -> bool:
        """is_their_placement

        Args:
            command (Referee_Info.Command.ValueType)

        Returns:
            bool: True if command is their placement.
        """
        return (self.__observer.is_team_yellow and (command is REF_COMMAND.BALL_PLACEMENT_BLUE)) or (
            not self.__observer.is_team_yellow and (command is REF_COMMAND.BALL_PLACEMENT_YELLOW)
        )
