#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class GeometryData(object):
    # ˅

    # ˄

    def __init__(self, field, calib, models):

        self.__field = field

        self.__calib = calib

        self.__models = models

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        return "<GeometryData>"
        # ˄

    @property
    def calib(self):
        # ˅
        return self.__calib
        # ˄

    @property
    def field(self):
        # ˅
        return self.__field
        # ˄

    @property
    def models(self):
        # ˅
        return self.__models
        # ˄

    # ˅

    # ˄


# ˅

# ˄
