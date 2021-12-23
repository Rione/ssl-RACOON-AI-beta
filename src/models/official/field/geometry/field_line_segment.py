#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class FieldLineSegment(object):
    # ˅

    # ˄

    def __init__(self):

        self.__name = None

        # Start point of the line segment.
        self.__p1 = Vector2f(0, 0)

        # End point of the line segment.
        self.__p2 = Vector2f(0, 0)

        # Thickness of the line segment.
        self.__thickness = 0

        # Undefined = 0;
        # CenterCircle = 1;
        # TopTouchLine = 2;
        # BottomTouchLine = 3;
        # LeftGoalLine = 4;
        # RightGoalLine = 5;
        # HalfwayLine = 6;
        # CenterLine = 7;
        # LeftPenaltyStretch = 8;
        # RightPenaltyStretch = 9;
        # LeftFieldLeftPenaltyStretch = 10;
        # LeftFieldRightPenaltyStretch = 11;
        # RightFieldLeftPenaltyStretch = 12;
        # RightFieldRightPenaltyStretch = 13;
        self.__type = 0

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def name(self):
        # ˅
        return self.__name
        # ˄

    @property
    def p1(self):
        # ˅
        return self.__p1
        # ˄

    @property
    def p2(self):
        # ˅
        return self.__p2
        # ˄

    @property
    def thickness(self):
        # ˅
        return self.__thickness
        # ˄

    @property
    def type(self):
        # ˅
        return self.__type
        # ˄

    # ˅

    # ˄


# ˅

# ˄
