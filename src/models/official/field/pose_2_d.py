#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅
from models.official.field.geometry.vector_2_f import Vector2f


# ˄


class Pose2D(Vector2f):
    # ˅
    
    # ˄

    def __init__(self, x, y, theta=0):

        # [rad]
        self.__theta = theta

        # ˅
        super().__init__(x, y)
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def theta(self):
        # ˅
        return self.__theta
        # ˄

    @theta.setter
    def theta(self, value):
        # ˅
        self.__theta = value
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
