#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅

# ˄


class SimCommand(object):
    # ˅
    
    # ˄

    def __init__(self):

        self.__timestamp = 0

        self.__isteamyellow = False

        self.__robot_commands = []

        # ˅
        pass
        # ˄

    @property
    def timestamp(self):
        # ˅
        return self.__timestamp
        # ˄

    @timestamp.setter
    def timestamp(self, value):
        # ˅
        self.__timestamp = value
        # ˄

    @property
    def isteamyellow(self):
        # ˅
        return self.__isteamyellow
        # ˄

    @isteamyellow.setter
    def isteamyellow(self, value):
        # ˅
        self.__isteamyellow = value
        # ˄

    @property
    def robot_commands(self):
        # ˅
        return self.__robot_commands
        # ˄

    @robot_commands.setter
    def robot_commands(self, value):
        # ˅
        self.__robot_commands = value
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
