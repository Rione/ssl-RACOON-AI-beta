#!/usr/bin/env python3.10

"""defense.py

    This module is for the defense class.
"""

from logging import getLogger
from math import tan
from typing import Optional

from numpy import sign

from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.movement.controls import Controls
from racoon_ai.observer import Observer
from racoon_ai.strategy.role import Role
from racoon_ai.strategy.subrole import SubRole


class Defense:
    """Defense
    Args:
        controls (Controls): Controls instance
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role, subrole: SubRole, controls: Controls) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        self.__role = role
        self.__subrole = subrole
        self.__controls = controls
        self.__send_cmds: list[RobotCommand]
        self.__enemy_offense: list[int] = []
        self.__defense_quantity: int = 0
        self.__max_robot_radius: float = 90
        self.__diff_defense_enemy_quantity: int = 0
        self.__enemy_quantity: int = 0
        self.__enemy_attacker: int = -1
        self.__count: int = 0

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmdsDefence

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def main(self) -> None:
        """main"""

        self.__send_cmds = []
        self.__defense_quantity = self.__role.get_defense_quantity
        self.__enemy_quantity = self.__observer.num_of_enemy_robots
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
                bot = self.__observer.get_our_by_id(self.__role.get_defense_id(i))
                if bot:
                    cmd = self.__default_position(bot, i)
                    self.__send_cmds.append(cmd)
        else:
            for i in range(self.__defense_quantity):
                bot = self.__observer.get_our_by_id(self.__role.get_defense_id(i))
                ene = self.__observer.get_enemy_by_id(self.__enemy_offense[i])
                if bot and ene:
                    cmd = self.__keep_penalty_area(bot, ene)
                    self.__send_cmds.append(cmd)

    def __enemy_offense_decide(self) -> None:
        """enemy_offense_decide"""

        defense_quantity: int = self.__defense_quantity
        enemy_offense: list[tuple[int, float, float]]

        enemy_offense = [
            (
                enemy.robot_id,
                MU.distance(enemy, self.__observer.geometry.goal),
                MU.radian(enemy, self.__observer.geometry.goal),
            )
            for enemy in self.__observer.enemy_robots
            if enemy.is_visible is True
        ]

        if self.__diff_defense_enemy_quantity >= 1:
            for _ in range(self.__diff_defense_enemy_quantity):
                enemy_offense.append(
                    (
                        self.__observer.enemy_robots[self.__enemy_attacker].robot_id,
                        MU.distance(self.__observer.enemy_robots[self.__enemy_attacker], self.__observer.geometry.goal),
                        MU.radian(self.__observer.enemy_robots[self.__enemy_attacker], self.__observer.geometry.goal),
                    )
                )

        if enemy_offense:
            enemy_offense.sort(reverse=False, key=lambda x: x[1])
            del enemy_offense[defense_quantity:]
            enemy_offense.sort(reverse=True, key=lambda x: x[2])
        self.__enemy_offense = list(row[0] for row in enemy_offense)

    def __keep_penalty_area(self, robot: Robot, enemy: Robot) -> RobotCommand:
        """keep_penalty_area"""
        radian_enemy_goal = MU.radian(enemy, self.__observer.geometry.goal)

        if abs(radian_enemy_goal) >= MU.PI / 2:
            radian_enemy_goal = (sign(radian_enemy_goal) * MU.PI) / 2

        if abs(radian_enemy_goal) < MU.PI / 4:
            target_pose = Pose(
                (self.__observer.geometry.goal.x + self.__observer.geometry.goal_width + self.__max_robot_radius),
                ((self.__observer.geometry.goal_width + self.__max_robot_radius) * tan(radian_enemy_goal)),
                radian_enemy_goal,
            )

        else:
            target_pose = Pose(
                (
                    self.__observer.geometry.goal.x
                    + (self.__observer.geometry.goal.y + self.__observer.geometry.goal_width + self.__max_robot_radius)
                    / tan(radian_enemy_goal)
                    * sign(radian_enemy_goal)
                ),
                (self.__observer.geometry.goal.y + (self.__observer.geometry.goal_width + self.__max_robot_radius))
                * sign(radian_enemy_goal),
                radian_enemy_goal,
            )

        if self.__diff_defense_enemy_quantity >= 1 and enemy.robot_id is self.__enemy_attacker:
            if abs(radian_enemy_goal) < MU.PI / 4:
                target_pose.y += self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
            else:
                target_pose.x -= (
                    self.__max_robot_radius * (self.__diff_defense_enemy_quantity - self.__count * 2)
                ) * sign(radian_enemy_goal)
            self.__count += 1

        command: RobotCommand = self.__controls.pid(target_pose, robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command

    def __default_position(self, robot: Robot, i: int) -> RobotCommand:
        """keep_penalty_area"""

        if self.__defense_quantity == 1:
            target_pose = Pose(
                (self.__observer.geometry.goal.x + self.__observer.geometry.goal_width + self.__max_robot_radius),
                self.__observer.geometry.goal_y,
                0,
            )

        else:
            target_pose = Pose(
                (self.__observer.geometry.goal.x + self.__observer.geometry.goal_width + self.__max_robot_radius),
                (
                    self.__observer.geometry.goal_width
                    - i * (self.__observer.geometry.goal_width * 2 / (self.__defense_quantity - 1))
                ),
                0,
            )

        command: RobotCommand = self.__controls.pid(target_pose, robot)
        return command
