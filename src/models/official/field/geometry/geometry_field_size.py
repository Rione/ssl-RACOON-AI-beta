#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# ˅

# ˄


class GeometryFieldSize(object):
    # ˅

    # ˄

    def __init__(
        self,
        field_length,
        field_width,
        goal_width,
        goal_depth,
        boundary_width,
        field_lines,
        field_arcs,
        penalty_area_depth,
        penalty_area_width,
    ):

        self.__field_length = field_length

        self.__field_width = field_width

        self.__goal_width = goal_width

        self.__goal_depth = goal_depth

        self.__boundary_width = boundary_width

        self.__field_lines = field_lines

        self.__field_arcs = field_arcs

        self.__penalty_area_depth = penalty_area_depth

        self.__penalty_area_width = penalty_area_width

        # ˅
        pass
        # ˄

    def __str__(self):
        # ˅
        pass
        # ˄

    @property
    def field_length(self):
        # ˅
        return self.__field_length
        # ˄

    @property
    def field_width(self):
        # ˅
        return self.__field_width
        # ˄

    @property
    def goal_width(self):
        # ˅
        return self.__goal_width
        # ˄

    @property
    def goal_depth(self):
        # ˅
        return self.__goal_depth
        # ˄

    @property
    def boundary_width(self):
        # ˅
        return self.__boundary_width
        # ˄

    @property
    def field_lines(self):
        # ˅
        return self.__field_lines
        # ˄

    @property
    def field_arcs(self):
        # ˅
        return self.__field_arcs
        # ˄

    @property
    def penalty_area_depth(self):
        # ˅
        return self.__penalty_area_depth
        # ˄

    @property
    def penalty_area_width(self):
        # ˅
        return self.__penalty_area_width
        # ˄

    # ˅

    # ˄


# ˅

# ˄
