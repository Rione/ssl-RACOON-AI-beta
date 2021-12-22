#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class FieldCircularArc(object):
    # ˅
    
    # ˄

    def __init__(self):

        # Name of this field marking.
        self.__name = None

        # Center point of the circular arc.
        self.__center = Vector2f(0,0)

        # Radius of the arc.
        self.__radius = 0

        # Start angle in counter-clockwise order.
        self.__a1 = 0

        # End angle in counter-clockwise order.
        self.__a2 = 0

        # Thickness of the arc.
        self.__thickness = 0

        # The type of this shape
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
    def center(self):
        # ˅
        return self.__center
        # ˄

    @property
    def radius(self):
        # ˅
        return self.__radius
        # ˄

    @property
    def a1(self):
        # ˅
        return self.__a1
        # ˄

    @property
    def a2(self):
        # ˅
        return self.__a2
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
