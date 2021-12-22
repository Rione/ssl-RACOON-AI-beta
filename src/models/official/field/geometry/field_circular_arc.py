#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅

# ˄


class FieldCircularArc(object):
    # ˅
    
    # ˄

    def __init__(self, name, center, radius, a1, a2, thickness, type):

        # Name of this field marking.
        self.__name = name

        # Center point of the circular arc.
        self.__center = center

        # Radius of the arc.
        self.__radius = radius

        # Start angle in counter-clockwise order.
        self.__a1 = a1

        # End angle in counter-clockwise order.
        self.__a2 = a2

        # Thickness of the arc.
        self.__thickness = thickness

        # The type of this shape
        self.__type = type

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
