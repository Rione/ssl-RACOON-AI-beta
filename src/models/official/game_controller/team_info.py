#!/usr/bin/env python


class TeamInfo(object):
    def __init__(
        self,
        name,
        score,
        red_cards,
        yellow_card_times,
        yellow_cards,
        timeouts,
        timeout_time,
        goalkeeper,
        foul_counter,
        ball_placement_failures,
        can_place_ball,
        max_allowed_bots,
        bot_substitution_intent,
        ball_placement_failures_reached,
    ):

        self.__name = name

        self.__score = score

        self.__red_cards = red_cards

        self.__yellow_card_times = yellow_card_times

        self.__yellow_cards = yellow_cards

        self.__timeouts = timeouts

        self.__timeout_time = timeout_time

        self.__goalkeeper = goalkeeper

        self.__foul_counter = foul_counter

        self.__ball_placement_failures = ball_placement_failures

        self.__can_place_ball = can_place_ball

        self.__max_allowed_bots = max_allowed_bots

        self.__bot_substitution_intent = bot_substitution_intent

        self.__ball_placement_failures_reached = ball_placement_failures_reached

    def __str__(self):
        pass
