#!/usr/bin/env python3.10

"""offense.py

    This module is for the Offense class.
"""

import math
from logging import getLogger

from racoon_ai.common import distance, move2pose, radian, radian_normalize
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.observer import Observer
from racoon_ai.strategy.role import Role


class Offense:
    """Offense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, observer: Observer, role: Role) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        self.__role = role
        self.__send_cmds: list[RobotCommand]
        self.__kick_flag: bool = False
        # self.__arrive_flag: bool = False

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
        bot = self.__observer.our_robots[self.__role.offense_ids[0]]
        cmd = self.__straight2ball(bot)
        self.__send_cmds.append(cmd)

        # (x,y)=(2000,2000)の地点に１番ロボットを移動させる
        bot = self.__observer.our_robots[1]
        target_position = Pose(2000, 2000, 0, radian(self.__observer.ball, bot))
        cmd = move2pose(bot, target_position)
        self.__logger.debug(cmd)
        self.__send_cmds.append(cmd)

    # def _pass_receive(self, robot: Robot) -> RobotCommand:
    #     command = RobotCommand(robot.robot_id)
    #     target_position = Point(0, 0, 0)
    #     distance_ball_robot = distance(self.__observer.our_robots[robot.robot_id], self.__observer.ball)

    #     if distance_ball_robot < 150:
    #         self.__kick_flag = False

    #     # if self.__kick_flag is True and self.__observer.get_ball_slope() != 0:
    #     #     target_position.x = (
    #     #         robot.y - self.__observer.get_ball_intercept() - (-1 / self.__observer.get_ball_slope()) * robot.x
    #     #     ) / (self.__observer.get_ball_slope() - (-1 / self.__observer.get_ball_slope()))
    #     #     target_position.y = (
    #     #         self.__observer.get_ball_slope() * target_position.x + self.__observer.get_ball_intercept()
    #     #     )
    #     angular = radian_normalize(radian(self.__observer.ball, robot) - robot.theta)

    #     radian_target_robot = radian_normalize(radian(target_position, robot) - robot.theta)
    #     distance_target_robot = distance(target_position, robot)
    #     speed = distance_target_robot / 1000

    #     fwd = math.cos(radian_target_robot) * speed
    #     sway = math.sin(radian_target_robot) * speed

    #     command.vel_fwd = fwd
    #     command.vel_sway = sway
    #     command.vel_angular = angular
    #     command.dribble_pow = 1
    #     command.kickpow = 0

    #     return command

    def __straight2ball(self, robot: Robot) -> RobotCommand:
        """straight2ball"""
        radian_ball_robot = radian_normalize(radian(self.__observer.ball, robot) - robot.theta)
        distance_target_robot = distance(self.__observer.ball, robot)
        speed = distance_target_robot / 1000.0

        dribble_power = 0.0
        # スピード制限
        if speed >= 1.0:
            speed = 1.0
        else:
            dribble_power = 1.0

        command = RobotCommand(0)
        command.vel_fwd = math.cos(radian_ball_robot) * speed
        command.vel_sway = math.sin(radian_ball_robot) * speed
        command.vel_angular = radian_ball_robot
        command.dribble_pow = dribble_power
        command.kickpow = 0
        return command
