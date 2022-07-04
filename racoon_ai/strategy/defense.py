#!/usr/bin/env python3.10

"""defense.py

    This module contains:
        - Defense
"""

from logging import getLogger
from math import tan
from typing import Optional

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Point, Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement import Controls
from racoon_ai.observer import Observer

from .base import StrategyBase
from .role import Role
from .subrole import SubRole


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
        self.__logger.info("Initializing...")

        self.__subrole: SubRole = subrole

        self.__enemy_offense: list[int] = []
        self.__defense_quantity: int = 0
        self.__max_robot_radius: float = 90
        self.__diff_defense_enemy_quantity: int = 0
        self.__enemy_quantity: int = 0
        self.__enemy_attacker: int = -1
        self.__count: int = 0
        self.__goal: Point = self.__observer.geometry.their_goal
        self.__their_goal: Point = self.__observer.geometry.goal
        self.__attack_direction: float = -1

    def main(self) -> None:
        """main"""
        self.send_cmds = []
        self.__defense_quantity = self.role.get_defense_quantity
        self.__enemy_quantity = self.observer.num_of_enemy_robots
        self.__diff_defense_enemy_quantity = self.__defense_quantity - (self.__enemy_quantity - 1)
        self.__enemy_attacker = self.__subrole.enemy_attacker_id
        self.__count = 0
        bot: Optional[Robot]
        ene: Optional[Robot]
        cmd: RobotCommand

        if self.__defense_quantity == 0:
            return

        # defenseのテスト動作
        self.__enemy_offense_decide()

        if self.__enemy_quantity <= 1:
            for i in range(self.__defense_quantity):
                bot = self.observer.get_our_by_id(self.role.get_defense_id(i))
                if bot:
                    cmd = self.__default_position(bot, i)
                    self.send_cmds.append(cmd)
        else:
            for i in range(self.__defense_quantity):
                bot = self.observer.get_our_by_id(self.role.get_defense_id(i))
                ene = self.observer.get_enemy_by_id(self.__enemy_offense[i])
                if bot and ene:
                    cmd = self.__keep_penalty_area(bot, ene)
                    self.send_cmds.append(cmd)

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
        self.__enemy_offense = list(row[0] for row in enemy_offense)

    def __keep_penalty_area(self, robot: Robot, enemy: Robot) -> RobotCommand:
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

        if self.__diff_defense_enemy_quantity >= 1 and enemy.robot_id is self.__enemy_attacker:
            if abs(radian_enemy_goal) < MU.PI / 4:
                target_pose.y += self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
            else:
                target_pose.x -= (
                    self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
                ) * sign(radian_enemy_goal)
            self.__count += 1

        command: RobotCommand = self.controls.pid(target_pose, robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command

    def __default_position(self, robot: Robot, i: int) -> RobotCommand:
        """keep_penalty_area"""

        target_pose: Pose
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

        return self.controls.pid(target_pose, robot)
