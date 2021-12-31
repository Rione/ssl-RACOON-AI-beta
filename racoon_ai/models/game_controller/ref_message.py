#!/usr/bin/env python3.10

"""ref_message.py

    This module contains:
        - Stage
        - Command
        - MatchType
        - TeamInfo
        - GameEventProposalGroup
        - Referee

    See also:
        https://github.com/RoboCup-SSL/ssl-game-controller/blob/master/proto/ssl_gc_referee_message.proto
"""

from enum import Enum

from racoon_ai.models.game_controller.game_event import GameEvent
from racoon_ai.models.vision.detection_tracked import Vector2f


class Stage(Enum):
    """Stage"""

    # The first half is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    NORMAL_FIRST_HALF_PRE = 0

    # The first half of the normal game, before half time.
    NORMAL_FIRST_HALF = 1

    # The second half is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    NORMAL_HALF_TIME = 2

    # The second half of the normal game, after half time.
    NORMAL_SECOND_HALF_PRE = 3

    # The break before extra time.
    NORMAL_SECOND_HALF = 4

    # The first half of extra time is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    EXTRA_TIME_BREAK = 5

    # The first half of extra time.
    EXTRA_FIRST_HALF_PRE = 6

    # The second half of extra time is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    EXTRA_FIRST_HALF = 7

    # The second half of extra time.
    EXTRA_HALF_TIME = 8

    # The break before penalty shootout.
    EXTRA_SECOND_HALF_PRE = 9

    EXTRA_SECOND_HALF = 10

    # The penalty shootout.
    PENALTY_SHOOTOUT_BREAK = 11

    PENALTY_SHOOTOUT = 12

    # The game is over.
    POST_GAME = 13


class Command(Enum):
    """Command"""

    # All robots should completely stop moving.
    HALT = 0

    # Robots must keep 50 cm from the ball.
    STOP = 1

    # A prepared kickoff or penalty may now be taken.
    NORMAL_START = 2

    # The ball is dropped and free for either team.
    FORCE_START = 3

    # The yellow team may move into kickoff position.
    PREPARE_KICKOFF_YELLOW = 4

    # The blue team may move into kickoff position.
    PREPARE_KICKOFF_BLUE = 5

    # The yellow team may move into penalty position.
    PREPARE_PENALTY_YELLOW = 6

    # The blue team may move into penalty position.
    PREPARE_PENALTY_BLUE = 7

    # The yellow team may take a direct free kick.
    DIRECT_FREE_YELLOW = 8

    # The blue team may take a direct free kick.
    DIRECT_FREE_BLUE = 9

    # The yellow team may take an indirect free kick.
    INDIRECT_FREE_YELLOW = 10

    # The blue team may take an indirect free kick.
    INDIRECT_FREE_BLUE = 11

    # The yellow team is currently in a timeout.
    TIMEOUT_YELLOW = 12

    # The blue team is currently in a timeout.
    TIMEOUT_BLUE = 13

    # The yellow team just scored a goal.
    # For information only.
    # For rules compliance, teams must treat as STOP.
    # Deprecated: Use the score field from the team infos instead.
    GOAL_YELLOW = 14

    # The blue team just scored a goal.
    GOAL_BLUE = 15

    # Equivalent to STOP, but the yellow team must pick up the ball and
    # move it into the Designated Position.
    BALL_PLACEMENT_YELLOW = 16

    # Equivalent to STOP, but the blue team must pick up the ball and
    # move it into the Designated Position.
    BALL_PLACEMENT_BLUE = 17

    NONE = -1


class MatchType(Enum):
    """MatchType"""

    # not set.
    UNKNOWN_MATCH = 0

    # match is part of the group phase
    GROUP_PHASE = 1

    # match is part of the elimination phase
    ELIMINATION_PHASE = 2

    # a friendly match, not part of a tournament
    FRIENDLY = 3


class TeamInfo:
    """TeamInfo

    Attributes:
        name (str):
            The team's name (empty string if operator has not typed anything).
        score (int):
            The number of goals scored by the team during normal play and overtime.
        red_cards (int):
            The number of red cards issued to the team since the beginning of the game.
        yellow_card_times (int):
            The amount of time (in microseconds) left on each yellow card issued
            to the team.
            If no yellow cards are issued, this array has no elements.
            Otherwise, times are ordered from smallest to largest.
        yellow_cards (int):
            The total number of yellow cards ever issued to the team.
        timeouts (int):
            The number of timeouts this team can still call.
            If in a timeout right now, that timeout is excluded.
        timeout_time (int):
            The number of microseconds of timeout this team can use.
        goalkeeper (int):
            The pattern number of this team's goalkeeper.
        foul_counter (int, optional):
            The total number of countable fouls that act towards yellow cards
        ball_placement_failures (int, optional):
            The number of consecutive ball placement failures of this team
        can_place_ball (bool, optional):
            Indicate if the team is able and allowed to place the ball
        max_allowed_bots (int, optional):
            The maximum number of bots allowed on the field based on division and cards
        bot_substitution_intent (bool, optional):
            The team has submitted an intent to substitute one or more robots
            at the next chance
        ball_placement_failuer_reached (bool, optional):
            Indicate if the team reached the maximum allowed ball placement failures
            and is thus not allowed to place the ball anymore
    """

    def __init__(
        self,
        name: str,
        score: int,
        red_cards: int,
        yellow_card_times: int,
        yellow_cards: int,
        timeouts: int,
        timeout_time: int,
        goalkeeper: int,
        foul_counter: int = 0,
        ball_placement_failures: int = 0,
        can_place_ball: bool = True,
        max_allowed_bots: int = 11,
        bot_substitution_intent: bool = False,
        ball_placement_failures_reached: bool = False,
    ) -> None:

        self.__name: str = name

        self.__score: int = score

        self.__red_cards: int = red_cards

        self.__yellow_card_times: int = yellow_card_times

        self.__yellow_cards: int = yellow_cards

        self.__timeouts: int = timeouts

        self.__timeout_time: int = timeout_time

        self.__goalkeeper: int = goalkeeper

        self.__foul_counter: int = foul_counter

        self.__ball_placement_failures: int = ball_placement_failures

        self.__can_place_ball: bool = can_place_ball

        self.__max_allowed_bots: int = max_allowed_bots

        self.__bot_substitution_intent: bool = bot_substitution_intent

        self.__ball_placement_failures_reached: bool = ball_placement_failures_reached

    @property
    def name(self) -> str:
        """name

        Returns:
            str: The team's name (empty string if operator has not typed anything).
        """
        return self.__name

    @property
    def score(self) -> int:
        """score

        Returns:
            int: The number of goals scored by the team during normal play and overtime.
        """
        return self.__score

    @property
    def red_cards(self) -> int:
        """red_cards

        Returns:
            int: The number of red cards issued to the team since the beginning
        """
        return self.__red_cards

    @property
    def yellow_card_times(self) -> int:
        """yellow_card_times

        Returns:
            int: The amount of time (in microseconds) left on each yellow card issued
            If no yellow cards are issued, this array has no elements.
            Otherwise, times are ordered from smallest to largest.
        """
        return self.__yellow_card_times

    @property
    def yellow_cards(self) -> int:
        """yellow_cards

        Returns:
            int: The total number of yellow cards ever issued to the team.
        """
        return self.__yellow_cards

    @property
    def timeouts(self) -> int:
        """timeouts

        Returns:
            int: The number of timeouts this team can still call.
            If in a timeout right now, that timeout is excluded.
        """
        return self.__timeouts

    @property
    def timeout_time(self) -> int:
        """timeout_time

        Returns:
            int: The number of microseconds of timeout this team can use.
        """
        return self.__timeout_time

    @property
    def goalkeeper(self) -> int:
        """goalkeeper

        Returns:
            int: The pattern number of this team's goalkeeper.
        """
        return self.__goalkeeper

    @property
    def foul_counter(self) -> int:
        """foul_counter

        Returns:
            int: The total number of countable fouls that act towards yellow cards
        """
        return self.__foul_counter

    @property
    def ball_placement_failures(self) -> int:
        """ball_placement_failures

        Returns:
            int: The number of consecutive ball placement failures of this team
        """
        return self.__ball_placement_failures

    @property
    def can_place_ball(self) -> bool:
        """can_place_ball

        Returns:
            bool: Indicate if the team is able and allowed to place the ball
        """
        return self.__can_place_ball

    @property
    def max_allowed_bots(self) -> int:
        """max_allowed_bots

        Returns:
            int: The maximum number of bots allowed on the field based on division/cards
        """
        return self.__max_allowed_bots

    @property
    def bot_substitution_intent(self) -> bool:
        """bot_substitution_intent

        Returns:
            bool: The team has submitted an intent to substitute one or more robots next
        """
        return self.__bot_substitution_intent

    @property
    def ball_placement_failures_reached(self) -> bool:
        """ball_placement_failures_reached

        Returns:
            bool: Indicate if the team reached the maximum allowed ball placement
                failures and is thus not allowed to place the ball anymore
        """
        return self.__ball_placement_failures_reached


class GameEventProposalGroup:
    """GameEventProposalGroup

    Attributes:
        game_event (GameEvent):
            The game event that this proposal group is for
        accepted (bool):
            Indicate if the proposal group has been accepted
    """

    def __init__(
        self,
        game_event: list[GameEvent] = [],
        accepted: bool = False,
    ) -> None:

        self.__game_event: list[GameEvent] = game_event

        self.__accepted: bool = accepted

    @property
    def game_event(self) -> list[GameEvent]:
        """game_event

        Returns:
            list[GameEvent]: The game event that this proposal group is for
        """
        return self.__game_event

    @property
    def accepted(self) -> bool:
        """accepted

        Returns:
            bool: Indicate if the proposal group has been accepted
        """
        return self.__accepted


class Referee:
    """Referee

    Attributes:
        packet_timestamp (int):
            The UNIX timestamp when the packet was sent, in microseconds.
            Divide by 1,000,000 to get a time_t.
        stage (Stage):
            The current stage of the game.
        stage_time_left (int, optional):
            The number of microseconds left in the stage.
            The following stages have this value; the rest do not:
                - NORMAL_FIRST_HALF
                - NORMAL_FIRST_HALF
                - NORMAL_SECOND_HALF
                - EXTRA_TIME_BREAK
                - EXTRA_FIRST_HALF
                - EXTRA_HALF_TIME
                - EXTRA_SECOND_HALF
                - PENALTY_SHOOTOUT_BREAK

            If the stage runs over its specified time, this value
            becomes negative.
        command (Command):
            The current command.
        command_counter (int):
            The number of commands issued since startup (mod 2^32).
        command_timestamp (int):
            The UNIX timestamp when the command was issued, in microseconds.
            This value changes only when a new command is issued, not on each packet.
        yellow (TeamInfo):
            Information about the yellow team.
        blue (TeamInfo):
            Information about the blue team.
        designated_position (Vector2f, optional):
            The position of the designated position.
        blue_team_on_positive_half (bool, optional):
            Information about the direction of play.
            True, if the blue team will have it's goal on the positive x-axis of the
            ssl-vision coordinate system.
            Obviously, the yellow team will play on the opposite half.
        next_command (Command, optional):
            The next command.
        current_action_time_remaining (int, optional):
            The time in microseconds that is remaining until the current action
            times out
            The time will not be reset. It can get negative.
            An autoRef would raise an appropriate event, if the time gets negative.
            Possible actions where this time is relevant:
                - free kicks
                - kickoff, penalty kick, force start
                - ball placement
        game_events (list[GameEvent]):
            All game events that were detected since the last RUNNING state.
            Will be cleared as soon as the game is continued.
        game_event_proposals (GameEventProposalGroup):
            All non-finished proposed game events that may be processed next.
        source_identifier (str, optional):
            A random UUID of the source that is kept constant at the source
            while running
            If multiple sources are broadcasting to the same network,
            this id can be used to identify individual sources
        match_type (MatchType, optional):
            The match type is a meta information about the current match
            that helps to process the logs after a competition
    """

    def __init__(
        self,
        packet_timestamp: int,
        stage: Stage,
        stage_time_left: int,
        command: Command,
        command_counter: int,
        command_timestamp: int,
        yellow: TeamInfo,
        blue: TeamInfo,
        designated_position: Vector2f = Vector2f(0, 0),
        blue_team_on_positive_half: bool = False,
        next_command: Command = Command.NONE,
        current_action_time_remaining: int = 0,
        game_events: list[GameEvent] = [],
        game_event_proporsals: GameEventProposalGroup = GameEventProposalGroup(),
        source_identifier: str = "",
        match_type: MatchType = MatchType.UNKNOWN_MATCH,
    ) -> None:

        self.__packet_timestamp: int = packet_timestamp

        self.__stage: Stage = stage

        self.__stage_time_left: int = stage_time_left

        self.__command: Command = command

        self.__command_counter: int = command_counter

        self.__command_timestamp: int = command_timestamp

        self.__yellow: TeamInfo = yellow

        self.__blue: TeamInfo = blue

        self.__designated_position: Vector2f = designated_position

        self.__blue_team_on_positive_half: bool = blue_team_on_positive_half

        self.__next_command: Command = next_command

        self.__current_action_time_remaining: int = current_action_time_remaining

        self.__game_events: list[GameEvent] = game_events

        self.__game_event_proporsals: GameEventProposalGroup = game_event_proporsals

        self.__source_identifier: str = source_identifier

        self.__match_type: MatchType = match_type

    @property
    def packet_timestamp(self) -> int:
        """packet_timestamp

        Returns:
            int: The UNIX timestamp when the packet was sent, in microseconds.
                Divide by 1,000,000 to get a time_t.
        """
        return self.__packet_timestamp

    @property
    def stage(self) -> Stage:
        """stage

        Returns:
            Stage: The current stage of the game.
        """
        return self.__stage

    @property
    def stage_time_left(self) -> int:
        """stage_time_left

        Returns:
            int: The number of microseconds left in the stage.
                The following stages have this value; the rest do not:
                    - NORMAL_FIRST_HALF
                    - NORMAL_FIRST_HALF
                    - NORMAL_SECOND_HALF
                    - EXTRA_TIME_BREAK
                    - EXTRA_FIRST_HALF
                    - EXTRA_HALF_TIME
                    - EXTRA_SECOND_HALF
                    - PENALTY_SHOOTOUT_BREAK

                If the stage runs over its specified time, this value
                becomes negative.
        """
        return self.__stage_time_left

    @property
    def command(self) -> Command:
        """command

        Returns:
            Command: The current command.
        """
        return self.__command

    @property
    def command_counter(self) -> int:
        """command_counter

        Returns:
            int: The number of commands issued since startup (mod 2^32).
        """
        return self.__command_counter

    @property
    def command_timestamp(self) -> int:
        """command_timestamp

        Returns:
            int: The UNIX timestamp when the command was issued, in microseconds.
                This value changes only when a new command is issued, not on each packet
        """
        return self.__command_timestamp

    @property
    def yellow(self) -> TeamInfo:
        """yellow

        Returns:
            TeamInfo: Information about the yellow team.
        """
        return self.__yellow

    @property
    def blue(self) -> TeamInfo:
        """blue

        Returns:
            TeamInfo: Information about the blue team.
        """
        return self.__blue

    @property
    def designated_position(self) -> Vector2f:
        """designated_position

        Returns:
            Vector2f: The position of the designated position.
        """
        return self.__designated_position

    @property
    def blue_team_on_positive_half(self) -> bool:
        """blue_team_on_positive_half

        Returns:
            bool: Information about the direction of play.
                True, if the blue team will have it's goal on the positive x-axis of the
                ssl-vision coordinate system.
                Obviously, the yellow team will play on the opposite half.
        """
        return self.__blue_team_on_positive_half

    @property
    def next_command(self) -> Command:
        """next_command

        Returns:
            Command: The next command.
        """
        return self.__next_command

    @property
    def current_action_time_remaining(self) -> int:
        """current_action_time_remaining

        Returns:
            int: The time in microseconds that is remaining until the current action
                times out
                The time will not be reset. It can get negative.
                An autoRef would raise an appropriate event, if the time gets negative.
                Possible actions where this time is relevant:
                    - free kicks
                    - kickoff, penalty kick, force start
                    - ball placement
        """
        return self.__current_action_time_remaining

    @property
    def game_events(self) -> list[GameEvent]:
        """game_events

        Returns:
            list[GameEvent]: All non-finished game events that may be processed next.
        """
        return self.__game_events

    @property
    def game_event_proporsals(self) -> GameEventProposalGroup:
        """game_event_proporsals

        Returns:
            GameEventProposalGroup: All game event proposals that may be processed next.
        """
        return self.__game_event_proporsals

    @property
    def source_identifier(self) -> str:
        """source_identifier

        Returns:
            str: The source identifier of the packet.
        """
        return self.__source_identifier

    @property
    def match_type(self) -> MatchType:
        """match_type

        Returns:
            MatchType: The match type.
        """
        return self.__match_type
