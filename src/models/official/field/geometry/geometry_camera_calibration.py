#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅

# ˄


class GeometryCameraCalibration(object):
    # ˅

    # ˄

    def __init__(
        self,
        camera_id,
        focal_length,
        principal_point_x,
        principal_point_y,
        distortion,
        q0,
        q1,
        q2,
        q3,
        tx,
        ty,
        tz,
    ):

        self.__camera_id = camera_id

        self.__focal_length = focal_length

        self.__principal_point_x = principal_point_x

        self.__principal_point_y = principal_point_y

        self.__distortion = distortion

        self.__q0 = q0

        self.__q1 = q1

        self.__q2 = q2

        self.__q3 = q3

        self.__tx = tx

        self.__ty = ty

        self.__tz = tz

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def principal_point_x(self):
        # ˅
        return self.__principal_point_x
        # ˄

    @property
    def principal_point_y(self):
        # ˅
        return self.__principal_point_y
        # ˄

    @property
    def distortion(self):
        # ˅
        return self.__distortion
        # ˄

    @property
    def q0(self):
        # ˅
        return self.__q0
        # ˄

    @property
    def camera_id(self):
        # ˅
        return self.__camera_id
        # ˄

    @property
    def tz(self):
        # ˅
        return self.__tz
        # ˄

    @property
    def q2(self):
        # ˅
        return self.__q2
        # ˄

    @property
    def focal_length(self):
        # ˅
        return self.__focal_length
        # ˄

    @property
    def q3(self):
        # ˅
        return self.__q3
        # ˄

    @property
    def ty(self):
        # ˅
        return self.__ty
        # ˄

    @property
    def tx(self):
        # ˅
        return self.__tx
        # ˄

    @property
    def q1(self):
        # ˅
        return self.__q1
        # ˄

    # ˅

    # ˄


# ˅

# ˄
