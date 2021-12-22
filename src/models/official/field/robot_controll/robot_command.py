#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅

# ˄


class RobotCommand(object):
    # ˅
    
    # ˄

    def __init__(self, id, kickspeedx, kickspeedz, veltangent, velnormal, velangular, spinner, wheelsspeed, wheel1, wheel2, wheel3, wheel4):

        self.__id = id

        self.__kickspeedx = kickspeedx

        self.__kickspeedz = kickspeedz

        self.__veltangent = veltangent

        self.__velnormal = velnormal

        self.__velangular = velangular

        self.__spinner = spinner

        self.__wheelsspeed = wheelsspeed

        self.__wheel1 = wheel1

        self.__wheel2 = wheel2

        self.__wheel3 = wheel3

        self.__wheel4 = wheel4

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def id(self):
        # ˅
        return self.__id
        # ˄

    @id.setter
    def id(self, value):
        # ˅
        self.__id = value
        # ˄

    @property
    def kickspeedx(self):
        # ˅
        return self.__kickspeedx
        # ˄

    @kickspeedx.setter
    def kickspeedx(self, value):
        # ˅
        self.__kickspeedx = value
        # ˄

    @property
    def kickspeedz(self):
        # ˅
        return self.__kickspeedz
        # ˄

    @kickspeedz.setter
    def kickspeedz(self, value):
        # ˅
        self.__kickspeedz = value
        # ˄

    @property
    def veltangent(self):
        # ˅
        return self.__veltangent
        # ˄

    @veltangent.setter
    def veltangent(self, value):
        # ˅
        self.__veltangent = value
        # ˄

    @property
    def velnormal(self):
        # ˅
        return self.__velnormal
        # ˄

    @velnormal.setter
    def velnormal(self, value):
        # ˅
        self.__velnormal = value
        # ˄

    @property
    def velangular(self):
        # ˅
        return self.__velangular
        # ˄

    @velangular.setter
    def velangular(self, value):
        # ˅
        self.__velangular = value
        # ˄

    @property
    def spinner(self):
        # ˅
        return self.__spinner
        # ˄

    @spinner.setter
    def spinner(self, value):
        # ˅
        self.__spinner = value
        # ˄

    @property
    def wheelsspeed(self):
        # ˅
        return self.__wheelsspeed
        # ˄

    @wheelsspeed.setter
    def wheelsspeed(self, value):
        # ˅
        self.__wheelsspeed = value
        # ˄

    @property
    def wheel1(self):
        # ˅
        return self.__wheel1
        # ˄

    @wheel1.setter
    def wheel1(self, value):
        # ˅
        self.__wheel1 = value
        # ˄

    @property
    def wheel2(self):
        # ˅
        return self.__wheel2
        # ˄

    @wheel2.setter
    def wheel2(self, value):
        # ˅
        self.__wheel2 = value
        # ˄

    @property
    def wheel3(self):
        # ˅
        return self.__wheel3
        # ˄

    @wheel3.setter
    def wheel3(self, value):
        # ˅
        self.__wheel3 = value
        # ˄

    @property
    def wheel4(self):
        # ˅
        return self.__wheel4
        # ˄

    @wheel4.setter
    def wheel4(self, value):
        # ˅
        self.__wheel4 = value
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
