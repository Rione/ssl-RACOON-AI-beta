#!/usr/bin/env python3.10

"""offense.py

    This module contains:
        - Offense
"""

from logging import getLogger
from math import cos, radians, sin
from typing import Optional

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from ..role import Role, SubRole
from .base import StrategyBase


class Offense(StrategyBase):
    """Offense(StrategyBase)

    Args:
        observer (Observer): Observer instance
        role (Role): Role instance
        subrole (SubRole): SubRole instance
        controls (Controls): Controls instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, subrole: SubRole, controls: Controls) -> None:
        super().__init__(observer, controls, role)

        self.__logger = getLogger(__name__)
        self.__logger.debug("Initializing...")

        self.__subrole: SubRole = subrole
        self.__offense_quantity: int = 0
        # self.__goal: Point = self.observer.geometry.goal
        # self.__their_goal: Point = self.observer.geometry.their_goal
        self.__attack_direction: float = self.observer.attack_direction

    def main(self, is_indirect: bool = False) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]

        for _, bot_id in enumerate(self.role.offense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                if bot.robot_id == self.__subrole.our_attacker_id:
                    if is_indirect:
                        self.pass_to_receiver()
                        continue
                    self.shoot_to_goal()
                    continue

                self.default_position()

    def direct_their(self) -> None:
        """direct_their"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]

        for _, bot_id in enumerate(self.role.offense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                if bot.robot_id == self.__subrole.our_attacker_id:
                    self.block_their_attacker()
                    continue

                self.default_position()

    def shoot_to_goal(self) -> None:
        """shoot_to_goal"""
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            cmd = self.controls.ball_around(self.observer.geometry.their_goal, bot)
            if bot.is_ball_catched:
                # if bot.distance_ball_robot <= 100 and bot.radian_ball_robot < 0.1:
                cmd.kickpow = 10
            cmd = self.controls.avoid_penalty_area(cmd, bot)
            cmd = self.controls.avoid_enemy(cmd, bot, self.observer.ball)
            cmd.dribble_pow = 0.0
            # close to ball
            cmd.dribble_pow = 0.0
            if bot.distance_ball_robot <= 600:
                if abs(bot.radian_ball_robot) < radians(30):
                    cmd.dribble_pow = 1.0
                cmd = self.controls.speed_limiter(cmd, 0.122)
            elif bot.distance_ball_robot <= 1500:
                cmd = self.controls.speed_limiter(cmd, 0.27)
            else:
                cmd = self.controls.speed_limiter(cmd, 0.4)
            self.send_cmds += [cmd]

    def pass_to_receiver(self) -> None:
        """pass_to_receiver"""
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            if receiver := self.observer.get_our_by_id(self.__subrole.receiver_id):
                cmd = self.controls.ball_around(receiver, bot)
                if bot.is_ball_catched:
                    # if bot.distance_ball_robot <= 100 and bot.radian_ball_robot < 0.1:
                    cmd.kickpow = 3
            elif enemy := self.observer.get_our_by_id(self.__subrole.enemy_attacker_id):
                cmd = self.controls.ball_around(enemy, bot)
                if bot.is_ball_catched:
                    # if bot.distance_ball_robot <= 100 and bot.radian_ball_robot < 0.1:
                    cmd.kickpow = 3
            else:
                cmd = self.controls.ball_around(Point(0, 0), bot)
                if bot.is_ball_catched:
                    # if bot.distance_ball_robot <= 100 and bot.radian_ball_robot < 0.1:
                    cmd.kickpow = 3
            cmd = self.controls.avoid_penalty_area(cmd, bot)
            cmd = self.controls.avoid_enemy(cmd, bot, self.observer.ball)
            cmd = self.controls.speed_limiter(cmd)
            self.send_cmds += [cmd]
            return

    def stop_offense(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        bot: Optional[Robot]
        cmd: RobotCommand

        # for i in self.role.offense_id_list:
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            cmd = RobotCommand(bot.robot_id)
            radian_goal_ball = MU.radian(self.observer.geometry.their_goal, self.observer.ball)
            radian_ball_robot = MU.radian(self.observer.ball, bot)
            target_pose = Pose(
                (self.observer.ball.x - 600 * cos(radian_goal_ball)),
                (self.observer.ball.y - 600 * sin(radian_goal_ball)),
                radian_ball_robot,
            )
            cmd = self.controls.pid(target_pose, bot)
            cmd = self.controls.avoid_ball(cmd, bot, self.observer.geometry.their_goal)
            cmd = self.controls.avoid_enemy(cmd, bot, self.observer.ball)
            cmd = self.controls.avoid_penalty_area(cmd, bot)
            cmd = self.controls.speed_limiter(cmd)
            self.send_cmds.append(cmd)

    def stop_attacker(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.send_cmds = []
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            cmd = self.controls.to_front_ball(self.observer.geometry.their_goal, bot, 500)
            cmd = self.controls.avoid_penalty_area(cmd, bot)
            cmd = self.controls.speed_limiter(cmd, 0.3)
            self.send_cmds.append(cmd)

    def penalty_kick(self, *, is_prepare: bool) -> None:
        """penalty_kick"""
        self.send_cmds = []
        cmd: RobotCommand
        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            if not is_prepare:
                self.shoot_to_goal()
                return

            cmd = self.controls.to_front_ball(self.observer.geometry.their_goal, bot)
            self.send_cmds += [cmd]

    def default_position(self) -> None:
        """default_position"""

        target_pose: Pose
        cmd: RobotCommand
        self.__offense_quantity = self.role.get_offense_quantity

        for i, bot_id in enumerate(self.role.offense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                if bot.robot_id != self.__subrole.our_attacker_id and self.__offense_quantity != 0:
                    target_pose = Pose(
                        (
                            self.observer.geometry.field_length
                            / 2
                            * (
                                1
                                - (self.__offense_quantity - 1 - ((i + 1) % max(self.__offense_quantity - 1, 1)))
                                / max(self.__offense_quantity, 2)
                            )
                        )
                        * self.__attack_direction
                        * sign(self.observer.ball.x * self.__attack_direction),
                        self.observer.geometry.field_width / 2
                        - (self.observer.geometry.field_width / (self.__offense_quantity + 1) * (i + 1)),
                        MU.radian(self.observer.ball, bot),
                    )
                    cmd = self.controls.pid(target_pose, bot)
                    cmd = self.controls.avoid_penalty_area(cmd, bot)
                    cmd = self.controls.avoid_enemy(cmd, bot, target_pose)
                    self.send_cmds += [cmd]

    def block_their_attacker(self) -> None:
        """block_their_attacker"""
        self.send_cmds = []
        cmd: RobotCommand

        if bot := self.observer.get_our_by_id(self.__subrole.our_attacker_id):
            if enemy := self.observer.get_enemy_by_id(self.__subrole.enemy_attacker_id):
                cmd = self.controls.to_front_ball(enemy, bot, 500)
                self.send_cmds += [cmd]
                return

            cmd = self.controls.to_front_ball(self.observer.geometry.goal, bot, 500)
            self.send_cmds += [cmd]
