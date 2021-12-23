#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅

# ˄


class Vector2f(object):
    # ˅

    # ˄

    def __init__(self, x, y):

        self.__x = x

        self.__y = y

        # ˅
        pass
        # ˄

    @property
    def x(self):
        # ˅
        return self.__x
        # ˄

    @x.setter
    def x(self, value):
        # ˅
        self.__x = value
        # ˄

    @property
    def y(self):
        # ˅
        return self.__y
        # ˄

    @y.setter
    def y(self, value):
        # ˅
        self.__y = value
        # ˄

    # ˅

    # ˄


# ˅

# ˄
