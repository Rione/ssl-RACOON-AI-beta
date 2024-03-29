#!/usr/bin/env python3.10

"""defense.py

    This module contains:
        - Defense
"""

from logging import getLogger
from math import tan

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from ..role import Role, SubRole
from .base import StrategyBase


class Defense(StrategyBase):
    """Defense(StrategyBase)

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
        self.__enemy_offense: list[int] = []  # pylint: disable=W0238
        self.__defense_quantity: int = 0
        self.__max_robot_radius: float = 90
        self.__diff_defense_enemy_quantity: int = 0
        self.__enemy_quantity: int = 0
        self.__enemy_attacker: int = -1
        self.__count: int = 0
        self.__goal: Point = self.observer.geometry.goal
        self.__their_goal: Point = self.observer.geometry.their_goal
        self.__attack_direction: float = self.observer.attack_direction

    def main(self) -> None:
        """main"""

        self.send_cmds = []
        self.__defense_quantity = self.role.get_defense_quantity
        self.__enemy_quantity = self.observer.num_of_enemy_vision_robots
        self.__diff_defense_enemy_quantity = self.__defense_quantity - (self.__enemy_quantity - 1)
        self.__enemy_attacker = self.__subrole.enemy_attacker_id
        self.__count = 0

        if self.__defense_quantity == 0:
            return

        # defenseのテスト動作
        self.__enemy_offense_decide()

        if self.__enemy_quantity <= 1:
            self.default_position()
            return

        # for i, bot_id in enumerate(self.role.defense_id_list):
        #     bot: Optional[Robot]
        #     if bot := self.observer.get_our_by_id(bot_id):
        #         cmd: RobotCommand
        #         ene: Optional[Robot]
        #         if ene := self.observer.get_enemy_by_id(self.__enemy_offense[i]):
        #             cmd = self.__keep_penalty_area(bot, ene)
        #             self.send_cmds += [cmd]

        self.__keep_penalty_area_from_ball()

    def __enemy_offense_decide(self) -> None:
        """enemy_offense_decide"""

        defense_quantity: int = self.__defense_quantity
        enemy_offense: list[tuple[int, float, float]]

        enemy_offense = [
            (
                enemy.robot_id,
                MU.distance(enemy, self.__goal),
                MU.radian_reduce(MU.radian(enemy, self.__goal), MU.radian(self.__their_goal, self.__goal))
                * self.__attack_direction,
            )
            for enemy in self.observer.enemy_robots
            if enemy.is_visible is True
        ]

        if self.__diff_defense_enemy_quantity >= 1:
            for _ in range(self.__diff_defense_enemy_quantity):
                enemy_offense.append(
                    (
                        self.observer.enemy_robots[self.__enemy_attacker].robot_id,
                        MU.distance(self.observer.enemy_robots[self.__enemy_attacker], self.__goal),
                        MU.radian_reduce(
                            MU.radian(self.observer.enemy_robots[self.__enemy_attacker], self.__goal),
                            MU.radian(self.__their_goal, self.__goal),
                        )
                        * self.__attack_direction,
                    )
                )

        if enemy_offense:
            enemy_offense.sort(reverse=False, key=lambda x: x[1])
            del enemy_offense[defense_quantity:]
            enemy_offense.sort(reverse=True, key=lambda x: x[2])
        self.__enemy_offense = list(row[0] for row in enemy_offense)  # pylint: disable=W0238

    def __keep_penalty_area(self, robot: Robot, enemy: Robot) -> RobotCommand:  # pylint: disable=W0238
        """keep_penalty_area"""
        radian_enemy_goal = (
            MU.radian_reduce(MU.radian(enemy, self.__goal), MU.radian(self.__their_goal, self.__goal))
            * self.__attack_direction
        )
        radian_enemy_robot = MU.radian(enemy, robot)

        if abs(radian_enemy_goal) >= MU.PI / 2:
            radian_enemy_goal = (sign(radian_enemy_goal) * MU.PI) / 2

        if abs(radian_enemy_goal) < MU.PI / 4:
            target_pose = Pose(
                (
                    self.__goal.x
                    + (self.observer.geometry.goal_width + self.__max_robot_radius) * self.__attack_direction
                ),
                ((self.observer.geometry.goal_width + self.__max_robot_radius) * tan(radian_enemy_goal)),
                radian_enemy_robot,
            )

        else:
            target_pose = Pose(
                (
                    self.__goal.x
                    + (self.__goal.y + self.observer.geometry.goal_width + self.__max_robot_radius)
                    / tan(radian_enemy_goal)
                    * sign(radian_enemy_goal)
                    * self.__attack_direction
                ),
                (self.__goal.y + (self.observer.geometry.goal_width + self.__max_robot_radius))
                * sign(radian_enemy_goal),
                radian_enemy_robot,
            )

        if (1 <= self.__diff_defense_enemy_quantity) and (enemy.robot_id is self.__enemy_attacker):
            if abs(radian_enemy_goal) < MU.PI / 4:
                target_pose.y += self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
            else:
                target_pose.x += (
                    self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
                ) * sign(radian_enemy_goal)
            self.__count += 1

        return self.controls.pid(target_pose, robot)

    def __keep_penalty_area_from_ball(self) -> None:
        """keep_penalty_areafrom_ball"""

        for i, bot_id in enumerate(self.role.defense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                radian_ball_goal = (
                    MU.radian_reduce(
                        MU.radian(self.observer.ball, self.__goal), MU.radian(self.__their_goal, self.__goal)
                    )
                    * self.__attack_direction
                )
                radian_enemy_robot = MU.radian(self.observer.ball, bot)

                if abs(radian_ball_goal) >= MU.PI / 2:
                    radian_ball_goal = (sign(radian_ball_goal) * MU.PI) / 2

                if abs(radian_ball_goal) < MU.PI / 4:
                    target_pose = Pose(
                        (
                            self.__goal.x
                            + (self.observer.geometry.goal_width + self.__max_robot_radius) * self.__attack_direction
                        ),
                        ((self.observer.geometry.goal_width + self.__max_robot_radius) * tan(radian_ball_goal)),
                        radian_enemy_robot,
                    )

                else:
                    target_pose = Pose(
                        (
                            self.__goal.x
                            + (self.__goal.y + self.observer.geometry.goal_width + self.__max_robot_radius)
                            / tan(radian_ball_goal)
                            * sign(radian_ball_goal)
                            * self.__attack_direction
                        ),
                        (self.__goal.y + (self.observer.geometry.goal_width + self.__max_robot_radius))
                        * sign(radian_ball_goal),
                        radian_enemy_robot,
                    )
                if abs(radian_ball_goal) < MU.PI / 4:
                    target_pose.y += self.__max_robot_radius * (self.__defense_quantity - i * 2)
                else:
                    target_pose.x += (self.__max_robot_radius * (self.__defense_quantity - i * 2)) * sign(
                        radian_ball_goal
                    )

                cmd = self.controls.pid(target_pose, bot)
                cmd = self.controls.avoid_penalty_area(cmd, bot, 30)
                self.send_cmds += [cmd]

    def default_position(self) -> None:
        """keep_penalty_area"""
        target_pose: Pose
        cmd: RobotCommand
        self.send_cmds = []
        self.__defense_quantity = self.role.get_defense_quantity

        for i, bot_id in enumerate(self.role.defense_id_list):
            if bot := self.observer.get_our_by_id(bot_id):
                if self.__defense_quantity == 1:
                    target_pose = Pose(
                        (
                            self.__goal.x
                            + (self.observer.geometry.goal_width + self.__max_robot_radius) * self.__attack_direction
                        ),
                        self.__goal.y,
                        MU.radian(self.__their_goal, self.__goal),
                    )

                else:
                    target_pose = Pose(
                        (
                            self.__goal.x
                            + (self.observer.geometry.goal_width + self.__max_robot_radius) * self.__attack_direction
                        ),
                        (
                            self.observer.geometry.goal_width
                            - i * (self.observer.geometry.goal_width * 2 / (self.__defense_quantity - 1))
                        ),
                        MU.radian(self.__their_goal, self.__goal),
                    )
                cmd = self.controls.pid(target_pose, bot)
                self.send_cmds += [cmd]
