#!/usr/bin/env python3.10

"""referee.py

    This module contains
        - Referee
"""

from typing import Optional, TypeAlias

from racoon_ai.models.coordinate import Point
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Referee_Info

REF_COMMAND: TypeAlias = Referee_Info.Command
REF_STAGE: TypeAlias = Referee_Info.Stage


class Referee:
    """
    Referee

    Attributes:
        command (Referee_Info.Command.ValueType): Command of the referee in integer.
        pre_command (Referee_Info.Command.ValueType, optional) = int of 1 time before command
        next_command (Referee_Info.Command.ValueType, optional) = int of 1 time after command
        stage (Referee_Info.Stage.ValueType) = Stage of the referee in integer.
        yellow_cards (int) = Number of yellow cards.
        red_cards (int) = Number of red cards.
        placement_designated_point (Point, optional) = designated Point of ball placement
    """

    def __init__(self) -> None:

        self.__command: REF_COMMAND.V = REF_COMMAND.HALT
        self.__pre_command: Optional[REF_COMMAND.V] = None
        self.__next_command: Optional[REF_COMMAND.V] = None
        self.__pre_one_command: Optional[REF_COMMAND.V] = None

        self.__stage: REF_STAGE.V = REF_STAGE.NORMAL_FIRST_HALF_PRE

        self.__yellow_cards: int = 0
        self.__red_cards: int = 0

        self.__placement_designated_point: Optional[Point] = None

    def __str__(self) -> str:
        msg: str = "("
        msg += f"cmd={self.command:d}(={self.command_str}), "
        msg += f"pre_cmd={self.pre_command:d}(={self.pre_command_str}), " if self.pre_command else ""
        msg += f"next_cmd={self.next_command:d}(={self.next_command_str}), " if self.next_command else ""
        msg += f"stage={self.stage:d}(={self.stage_str}), "
        msg += f"yellow={self.yellow_cards:d}, "
        msg += f"red={self.red_cards:d}, "
        msg += f"placement={self.placement_designated_point}" if self.placement_designated_point else ""
        msg += ")"
        return msg

    @property
    def command(self) -> "REF_COMMAND.V":
        """command

        Returns:
            Referee_Info.Command.ValueType: command in int
        """
        return self.__command

    @property
    def command_str(self) -> str:
        """command_str"""
        return Referee_Info.Command.Name(self.command)

    @property
    def pre_command(self) -> Optional["Referee_Info.Command.V"]:
        """pre_command"""
        return self.__pre_command

    @property
    def pre_one_command(self) -> Optional["Referee_Info.Command.V"]:
        """pre_one_command"""
        return self.__pre_one_command

    @property
    def pre_command_str(self) -> str:
        """pre_command_str"""
        return Referee_Info.Command.Name(self.pre_command) if self.pre_command else "#N/A"

    @property
    def next_command(self) -> Optional["Referee_Info.Command.V"]:
        """next_command"""
        return self.__next_command

    @property
    def next_command_str(self) -> str:
        """next_command_str"""
        return Referee_Info.Command.Name(self.next_command) if self.next_command else "#N/A"

    @property
    def stage(self) -> "Referee_Info.Stage.V":
        """stage

        Returns:
            Referee_Info.Stage.ValueType: stage in int
        """
        return self.__stage

    @property
    def stage_str(self) -> str:
        """stage_str"""
        return Referee_Info.Stage.Name(self.stage)

    @property
    def yellow_cards(self) -> int:
        """yellow_cards"""
        return self.__yellow_cards

    @property
    def red_cards(self) -> int:
        """red_cards"""
        return self.__red_cards

    @property
    def placement_designated_point(self) -> Optional[Point]:
        """ball_placement"""
        return self.__placement_designated_point

    def update(self, proto: Referee_Info) -> None:
        """
        Update robot

        Args:
            proto (Referee_Info): Referee_Info
        """
        self.__from_proto(proto)

    def __from_proto(self, proto: Referee_Info) -> None:
        """from_proto

        Args:
            proto (Referee_Info): Referee_Info
        """
        self.__pre_one_command = self.__command
        self.__command = proto.command
        self.__stage = proto.stage
        self.__yellow_cards = proto.yellow_cards
        self.__red_cards = proto.red_cards
        self.__pre_command = proto.pre_command if proto.pre_command else None
        self.__next_command = proto.next_command if proto.next_command else None
        self.__placement_designated_point = (
            Point(
                proto.ball_placement_x,
                proto.ball_placement_y,
            )
            if (proto.command is (REF_COMMAND.BALL_PLACEMENT_BLUE or REF_COMMAND.BALL_PLACEMENT_YELLOW))
            else None
        )

    @staticmethod
    def cmd_to_str(cmd: "REF_COMMAND.V") -> str:
        """cmd_to_str"""
        return REF_COMMAND.Name(cmd)

    @staticmethod
    def stage_to_str(stage: "REF_STAGE.V") -> str:
        """cmd_to_str"""
        return REF_STAGE.Name(stage)
