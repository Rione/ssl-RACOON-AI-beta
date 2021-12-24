#!/usr/bin/env python3.10


class RobotFeedback:
    def __init__(self, id, dribbler_ball_contact, custom):

        self.id = id

        self.dribbler_ball_contact = dribbler_ball_contact

        self.custom = custom

    def __str__(self):
        pass

    @property
    def id(self):
        return self.__id

    @property
    def dribbler_ball_contact(self):
        return self.__dribbler_ball_contact

    @property
    def custom(self):
        return self.__custom
