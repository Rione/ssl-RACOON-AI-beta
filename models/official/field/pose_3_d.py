#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
from models.official.field.pose_2_d import Pose2D


# ˄


class Pose3D(Pose2D):
    # ˅
    
    # ˄

    def __init__(self, x, y, theta, z):

        # [mm]
        self.__z = z

        # ˅
        super().__init__(x, y, theta)
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def z(self):
        # ˅
        return self.__z
        # ˄

    @z.setter
    def z(self, value):
        # ˅
        self.__z = value
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
