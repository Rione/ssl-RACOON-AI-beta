#!/usr/bin/env python3.10


class RobotControlResponse:
    def __init__(self, feedback):

        self.feedback = feedback

    def __str__(self):
        pass

    @property
    def feedback(self):
        return self.__feedback
