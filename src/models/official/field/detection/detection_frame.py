#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class DetectionFrame(object):
    # ˅

    # ˄

    def __init__(
        self,
        frame_number,
        t_capture,
        t_sent,
        camera_id,
        balls,
        robots_yellow,
        robots_blue,
    ):

        self.__frame_number = frame_number

        self.__t_capture = t_capture

        self.__t_sent = t_sent

        self.__camera_id = camera_id

        self.__balls = balls

        self.__robots_yellow = robots_yellow

        self.__robots_blue = robots_blue

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        # TODO: balls, robots_yellow, robots_blue
        return "DetectionFrame(%d, %.2f, %.2f, %d, %s, %s, %s)" % (
            self.__frame_number,
            self.__t_capture,
            self.__t_sent,
            self.__camera_id,
            "Undefined",
            "Undefined",
            "Undefined",
        )
        # ˄

    @property
    def frame_number(self):
        # ˅
        return self.__frame_number
        # ˄

    @property
    def t_capture(self):
        # ˅
        return self.__t_capture
        # ˄

    @property
    def t_sent(self):
        # ˅
        return self.__t_sent
        # ˄

    @property
    def camera_id(self):
        # ˅
        return self.__camera_id
        # ˄

    @property
    def balls(self):
        # ˅
        return self.__balls
        # ˄

    @property
    def robots_yellow(self):
        # ˅
        return self.__robots_yellow
        # ˄

    @property
    def robots_blue(self):
        # ˅
        return self.__robots_blue
        # ˄

    # ˅

    # ˄


# ˅

# ˄
