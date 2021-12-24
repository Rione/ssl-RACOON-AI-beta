#!/usr/bin/env python


class RobotControlResponse(object):
    def __init__(self, feedback):

        self.feedback = feedback

    def __str__(self):
        pass

    @property
    def feedback(self):
        return self.__feedback
