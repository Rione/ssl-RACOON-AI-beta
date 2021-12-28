#!/usr/bin/env python3.10

"""game_event.py

    This module contains:
        - EventType
        - GameEvent

    TODO:
        - Fill GameEvent class

    See also:
        https://github.com/RoboCup-SSL/ssl-game-controller/blob/master/proto/ssl_gc_game_event.proto
"""

from enum import Enum


class EventType(Enum):
    """EventType"""

    UNKNOWN_GAME_EVENT_TYPE = 0

    # Ball out of field events (stopping)
    BALL_LEFT_FIELD_TOUCH_LINE = 6  # triggered by autoRef
    BALL_LEFT_FIELD_GOAL_LINE = 7  # triggered by autoRef
    AIMLESS_KICK = 11  # triggered by autoRef

    # Stopping Fouls
    ATTACKER_TOO_CLOSE_TO_DEFENSE_AREA = 19  # triggered by autoRef
    DEFENDER_IN_DEFENSE_AREA = 31  # triggered by autoRef
    BOUNDARY_CROSSING = 41  # triggered by autoRef
    KEEPER_HELD_BALL = 13  # triggered by GC
    BOT_DRIBBLED_BALL_TOO_FAR = 17  # triggered by autoRef

    BOT_PUSHED_BOT = 24  # triggered by human ref
    BOT_HELD_BALL_DELIBERATELY = 26  # triggered by human ref
    BOT_TIPPED_OVER = 27  # triggered by human ref

    # Non-Stopping Fouls

    ATTACKER_TOUCHED_BALL_IN_DEFENSE_AREA = 15  # triggered by autoRef
    BOT_KICKED_BALL_TOO_FAST = 18  # triggered by autoRef
    BOT_CRASH_UNIQUE = 22  # triggered by autoRef
    BOT_CRASH_DRAWN = 21  # triggered by autoRef

    # Fouls while ball out of play

    DEFENDER_TOO_CLOSE_TO_KICK_POINT = 29  # triggered by autoRef
    BOT_TOO_FAST_IN_STOP = 28  # triggered by autoRef
    BOT_INTERFERED_PLACEMENT = 20  # triggered by autoRef

    # Scoring goals
    POSSIBLE_GOAL = 39  # triggered by autoRef
    GOAL = 8  # triggered by GC
    INVALID_GOAL = 42  # triggered by GC

    # Other events

    ATTACKER_DOUBLE_TOUCHED_BALL = 14  # triggered by autoRef
    PLACEMENT_SUCCEEDED = 5  # triggered by autoRef
    PENALTY_KICK_FAILED = 43  # triggered by GC and autoRef

    NO_PROGRESS_IN_GAME = 2  # triggered by GC
    PLACEMENT_FAILED = 3  # triggered by GC
    MULTIPLE_CARDS = 32  # triggered by GC
    MULTIPLE_FOULS = 34  # triggered by GC
    BOT_SUBSTITUTION = 37  # triggered by GC
    TOO_MANY_ROBOTS = 38  # triggered by GC
    CHALLENGE_FLAG = 44  # triggered by GC
    EMERGENCY_STOP = 45  # triggered by GC

    UNSPORTING_BEHAVIOR_MINOR = 35  # triggered by human ref
    UNSPORTING_BEHAVIOR_MAJOR = 36  # triggered by human ref

    # Deprecated events
    PREPARED = 1  # deprecated
    INDIRECT_GOAL = 9  # deprecated
    CHIPPED_GOAL = 10  # deprecated
    KICK_TIMEOUT = 12  # deprecated
    ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA = 16  # deprecated
    ATTACKER_TOUCHED_OPPONENT_IN_DEFENSE_AREA_SKIPPED = 40  # deprecated
    BOT_CRASH_UNIQUE_SKIPPED = 23  # deprecated
    BOT_PUSHED_BOT_SKIPPED = 25  # deprecated
    DEFENDER_IN_DEFENSE_AREA_PARTIALLY = 30  # deprecated
    MULTIPLE_PLACEMENT_FAILURES = 33  # deprecated


class GameEvent:
    """GameEvent

    Attributes:
    """

    def __init__(
        self,
        origin: str,
        type: EventType = EventType.UNKNOWN_GAME_EVENT_TYPE,
    ) -> None:

        self.__origin: str = origin

        self.__type: EventType = type
