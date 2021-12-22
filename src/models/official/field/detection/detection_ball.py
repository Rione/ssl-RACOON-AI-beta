#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅
from models.official.field.pose_3_d import Pose3D


# ˄


class DetectionBall(Pose3D):
    # ˅

    # ˄

    def __init__(self, confidence, area, pixel_x, pixel_y, x, y, z):

        self.__confidence = confidence

        self.__area = area

        self.__pixel_x = pixel_x

        self.__pixel_y = pixel_y

        # ˅
        Pose3D.__init__(self, x, y, 0, z)
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def confidence(self):
        # ˅
        return self.__confidence
        # ˄

    @property
    def area(self):
        # ˅
        return self.__area
        # ˄

    @property
    def pixel_x(self):
        # ˅
        return self.__pixel_x
        # ˄

    @property
    def pixel_y(self):
        # ˅
        return self.__pixel_y
        # ˄

    # ˅

    # ˄


# ˅

# ˄
