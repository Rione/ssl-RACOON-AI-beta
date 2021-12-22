#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class RobotCustomFeedback(object):
    # ˅

    # ˄

    def __init__(self, battery_vol, boosted_vol, encoder_vals):

        self.__battery_vol = battery_vol

        self.__boosted_vol = boosted_vol

        self.__encoder_vals = encoder_vals

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def battery_vol(self):
        # ˅
        return self.__battery_vol
        # ˄

    @property
    def boosted_vol(self):
        # ˅
        return self.__boosted_vol
        # ˄

    @property
    def encoder_vals(self):
        # ˅
        return self.__encoder_vals
        # ˄

    # ˅

    # ˄


# ˅

# ˄
