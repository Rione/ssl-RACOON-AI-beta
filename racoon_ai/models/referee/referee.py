#!/usr/bin/env python3.10

"""referee.py

    This module contains
        - Referee
"""

from racoon_ai.models.coordinate import Point
from racoon_ai.proto.pb_gen.to_racoonai_pb2 import Referee_Info


class Referee:
    """
    Referee

    Attributes:
        command (int) = int of command
        stage (int) = int of stage
        yellow_cards (int) = int of yellow cards
        red_cards (int) = int of red cards
        pre_command (int, optional) = int of 1 time before command
        next_command (int, optional) = int of 1 time after command
        placement_designated_point (Point, optional) = designated Point of ball placement
    """

    def __init__(self) -> None:
        self.__command: int = int(0)
        self.__stage: int = int(0)
        self.__yellow_cards: int = int(0)
        self.__red_cards: int = int(0)
        self.__pre_command: int = int(0)
        self.__next_command: int = int(0)
        self.__placement_designated_point: Point = Point(0, 0)

    def __str__(self) -> str:
        return (
            "Referee("
            f"command={self.cmd_to_str(self.command)}({self.command}),"
            f"stage={self.stage_to_str(self.stage)}({self.stage}),"
            f"yellow_cards={self.yellow_cards:2d},"
            f"red_cards={self.red_cards:2d},"
            f"pre_command={self.cmd_to_str(self.pre_command)}({self.pre_command}),"
            f"next_command={self.cmd_to_str(self.next_command)}({self.next_command}),"
            f"placement_designated_point={self.placement_designated_point}"
            ")"
        )

    @property
    def command(self) -> int:
        """command"""
        return self.__command

    @property
    def stage(self) -> int:
        """stage"""
        return self.__stage

    @property
    def yellow_cards(self) -> int:
        """yellow_cards"""
        return self.__yellow_cards

    @property
    def red_cards(self) -> int:
        """red_cards"""
        return self.__red_cards

    @property
    def pre_command(self) -> int:
        """pre_command"""
        return self.__pre_command

    @property
    def next_command(self) -> int:
        """next_command"""
        return self.__next_command

    @property
    def placement_designated_point(self) -> Point:
        """ball_placement"""
        return self.__placement_designated_point

    def update(self, referee: Referee_Info) -> None:
        """
        Update robot

        Args:
            referee (Referee_Info): Referee_Info
        """
        self.__from_proto(referee)

    def __from_proto(self, referee: Referee_Info) -> None:
        """from_proto

        Args:
            referee (Referee_Info): Referee_Info
        """
        self.__command = referee.command
        self.__stage = referee.stage
        self.__yellow_cards = referee.yellow_cards
        self.__red_cards = referee.red_cards
        self.__pre_command = referee.pre_command
        self.__next_command = referee.next_command
        self.__placement_designated_point = Point(referee.ball_placement_x, referee.ball_placement_y)

    @staticmethod
    def cmd_to_str(cmd: int) -> str:
        """cmd_to_str"""
        if cmd < 0:
            return "Undefined"
        commands: list[str] = Referee_Info.Command.keys()
        return commands[cmd]

    @staticmethod
    def stage_to_str(stage: int) -> str:
        """cmd_to_str"""
        if stage < 0:
            return "Undefined"
        stages: list[str] = Referee_Info.Stage.keys()
        return stages[stage]
