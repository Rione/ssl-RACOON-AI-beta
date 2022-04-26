#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

import math
from logging import getLogger

from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.observer import Observer


class Offense:
    """Offense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        # self.__role = role
        self.__send_cmds: list[RobotCommand]
        self.__kick_flag: bool = False
        # self.__arrive_flag: bool = False
        self.__our_goal: Point = Point(-6000, 0)

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    @property
    def kick_flag(self) -> bool:
        """kick_flag

        Returns:
            bool: kick_flag
        """
        return self.__kick_flag

    def main(self) -> None:
        """main"""
        # commandの情報を格納するリスト
        self.__send_cmds = []
        bot: Robot
        cmd: RobotCommand

        # 一番ボールに近いロボットがボールに向かって前進
        bot = self.__observer.our_robots[5]
        #if (
        #    distance(self.__observer.ball, bot) >= 150
        #    or abs(radian_normalize(radian(self.__our_goal, bot)) - radian_normalize(radian(self.__observer.ball, bot)))
        #    <= 0.1
        #):
        #    cmd = self.__straightball(bot)
        #elif distance(self.__observer.ball, bot) <= 105:
        #    cmd = self.__straightgoal(bot)
        #else:
        #    cmd = self.__ballaround(bot)

        #if abs(radian_normalize(radian(self.__our_goal, bot)) - radian_normalize(radian(self.__observer.ball, bot))) >= 0.1:
        #   cmd = self.__ballaround2(bot)
        #elif distance(self.__observer.ball, bot) <= 105:
        #    cmd = self.__straightgoal(bot)
        #else:
        #    cmd = self.__straightball(bot)

        cmd = self.__ballaround2(bot)
        print(bot.x)
        if abs(radian(self.__our_goal, bot) - bot.theta) < 0.1 and distance(self.__observer.ball, bot) <= 105:
            cmd.kickpow = 10
        # print(distance(self.__observer.ball, bot))
        self.__send_cmds.append(cmd)

    def __straightball(self, robot: Robot) -> RobotCommand:
        """straight2ball"""
        radian_ball_robot = radian_normalize(radian(self.__observer.ball, robot) - robot.theta)
        radian_goal_robot = radian_normalize(radian(self.__our_goal, robot) - robot.theta)
        distance_target_robot = distance(self.__observer.ball, robot)
        speed = distance_target_robot / 1000.0

        # スピード制限
        speed = min(speed, 1)

        command = RobotCommand(5)
        command.vel_fwd = math.cos(radian_ball_robot) * speed
        command.vel_sway = math.sin(radian_ball_robot) * speed
        command.vel_angular = radian_goal_robot
        command.dribble_pow = 0
        command.kickpow = 0
        return command

    def __straightgoal(self, robot: Robot) -> RobotCommand:
        """straight2ball"""
        radian_goal_robot = radian_normalize(radian(self.__our_goal, robot) - robot.theta)
        # distance_target_robot = distance(self.__our_goal, robot)
        speed = 0

        # スピード制限
        speed = min(speed, 1)

        command = RobotCommand(5)
        command.vel_fwd = math.cos(radian_goal_robot) * speed
        command.vel_sway = math.sin(radian_goal_robot) * speed
        command.vel_angular = radian_goal_robot
        command.dribble_pow = 1
        command.kickpow = 10
        return command

    def __ballaround(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_goal_robot = radian_normalize(radian(self.__our_goal, robot) - robot.theta)
        radian_around = radian_normalize(radian(self.__observer.ball, robot))
        discrimination = radian_normalize(
            radian_normalize(radian(robot, self.__observer.ball))
            - radian_normalize(radian(self.__our_goal, self.__observer.ball))
        )
        radian_around -= discrimination / abs(discrimination) * math.pi / 2
        radian_around -= robot.theta
        distance_target_robot = distance(self.__observer.ball, robot)
        speed = distance_target_robot / 2000

        # スピード制限
        speed = min(speed, 1)

        command = RobotCommand(5)
        command.vel_fwd = math.cos(radian_around) * speed
        command.vel_sway = math.sin(radian_around) * speed
        command.vel_angular = radian_goal_robot
        command.dribble_pow = 1
        command.kickpow = 0
        return command

    def __ballaround2(self, robot: Robot) -> RobotCommand:
        """ballaround"""
        radian_ball_robot = radian_normalize(radian(self.__observer.ball, robot) - robot.theta)
        radian_goal_robot = radian_normalize(radian(self.__our_goal, robot) - robot.theta)
        distance_target_robot = distance(self.__observer.ball, robot)
        adjustment = distance_target_robot / 900

        vel_fwd = math.cos(radian_ball_robot) * adjustment
        vel_sway = math.sin(radian_ball_robot) * adjustment

        radian_around = radian_normalize(radian(self.__observer.ball, robot))
        discrimination = radian_normalize(
          radian_normalize(radian(robot, self.__observer.ball))
          - radian_normalize(radian(self.__our_goal, self.__observer.ball))
        )
        radian_around -= discrimination / abs(discrimination) * math.pi / 2
        radian_around -= robot.theta
        adjustment = 100 / distance_target_robot

        vel_fwd += math.cos(radian_around) * adjustment
        vel_sway += math.sin(radian_around) * adjustment

        discrimination = radian_normalize(
          radian_normalize(radian(self.__observer.ball, robot))
          - radian_normalize(radian(self.__our_goal, robot))
        )
        adjustment = 0.1 / abs(discrimination)

        vel_fwd += math.cos(radian_ball_robot) * adjustment
        vel_sway += math.sin(radian_ball_robot) * adjustment

        adjustment = math.sqrt(vel_fwd*vel_fwd + vel_sway*vel_sway)
        speed = distance_target_robot / 1000.0
        speed = min(speed, 0.3)

        command = RobotCommand(5)
        command.vel_fwd = vel_fwd / adjustment * speed
        command.vel_sway = vel_sway / adjustment * speed
        command.vel_angular = radian_goal_robot
        command.dribble_pow = 0
        command.kickpow = 0
        return command
