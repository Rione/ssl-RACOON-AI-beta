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
from racoon_ai.networks.receiver import MWReceiver
from racoon_ai.strategy.role import Role


class Defense:
    """Defense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: MWReceiver, role: Role, controls: Controls) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        self.__role = role
        self.__controls = controls
        self.__send_cmds: list[RobotCommand]
        self.__enemy_offense: list[int] = []
        self.__max_robot_radius: float = 90

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmdsDefence

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def main(self) -> None:
        """main"""

        # commandの情報を格納するリスト
        self.__send_cmds = []
        bot: Optional[Robot]
        ene: Optional[Robot]
        cmd: RobotCommand

        # defenseのテスト動作
        self.__enemy_offense_decide()

        for i in range(self.__role.get_defense_quantity):
            bot = self.__observer.get_our_by_id(self.__role.get_defense_id(i))
            ene = self.__observer.get_enemy_by_id(self.__enemy_offense[i])
            if bot and ene:
                cmd = self.__keep_penalty_area(bot, ene)
                self.__send_cmds.append(cmd)

    def __enemy_offense_decide(self) -> None:
        """enemy_offense_decide"""

        defense_quantity: int = self.__role.get_defense_quantity
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
            print(self.__observer.geometry.goal.x)
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

        command: RobotCommand = self.__controls.pid(target_pose, robot)
        command.dribble_pow = 0
        command.kickpow = 0
        return command
