#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ˅
from models.official.field.pose_2_d import Pose2D
from models.official.field.robot_controll.robot_feedback import RobotFeedback


# ˄


class DetectionRobot(RobotFeedback, Pose2D):
    # ˅
    
    # ˄

    def __init__(self, confidence, robot_id, x, y, theta, pixel_x, pixel_y, height):

        self.__confidence = confidence

        self.__robot_id = robot_id

        self.__pixel_x = pixel_x

        self.__pixel_y = pixel_y

        self.__height = height

        # ˅
        Pose2D.__init__(self, x, y, theta)
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
    def robot_id(self):
        # ˅
        return self.__robot_id
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

    @property
    def height(self):
        # ˅
        return self.__height
        # ˄

    # ˅
    
    # ˄


# ˅

# ˄
