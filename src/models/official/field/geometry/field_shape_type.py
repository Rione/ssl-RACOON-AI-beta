#!/usr/bin/env python3.10

"""field_shape_type.py

    This module contains the FieldShapeType enum.
"""

from enum import Enum


class FieldShapeType(Enum):
    """FieldShapeType

    This enum represents the type of a field shape.
    """

    UNDEFINED = 0

    CENENTER_CIRCLE = 1

    TOP_TOUCHLINE = 2

    BOTTOM_TOUCHLINE = 3

    LEFT_GOALLINE = 4

    RIGHT_GOALLINE = 5

    HALFWAY_LINE = 6

    CENTER_LINE = 7

    LEFT_PENALTY_STRETCH = 8

    RIGHT_PENALTY_STRETCH = 9

    LEFT_FIELD_LEFT_PENALTY_STRETCH = 10

    LEFT_FIELD_RIGHT_PENALTY_STRETCH = 11

    RIGHT_FIELD_LEFT_PENALTY_STRETCH = 12

    RIGHT_FIELD_RIGHT_PENALTY_STRETCH = 13
