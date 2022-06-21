#!/usr/bin/env python3.10

"""defense.py

    This module is for the defense class.
"""

import math
from logging import getLogger

from common.controls import Controls

# from racoon_ai.common import distance, radian, radian_normalize
from racoon_ai.common.math_utils import MathUtils as MU
from racoon_ai.models.coordinate import Pose
from racoon_ai.models.robot import Robot, RobotCommand
from racoon_ai.networks.receiver import MWReceiver

# from racoon_ai.observer import Observer
# from racoon_ai.strategy.role import Role

# import sympy


class Defense:
    """Defense
    Args:
        observer (Observer): Observer instance

    Attributes:
        send_cmds (list[RobotCommand]): RobotCommand list.
    """

    def __init__(self, controls: Controls, observer: MWReceiver) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__observer = observer
        # self.__role = role
        self.__send_cmds: list[RobotCommand]
        self.__kick_flag: bool = False
        # self.__arrive_flag: bool = False
        self.__our_goal: Pose = Pose(-6000, 0)

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmdsDefence

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
        self.__observer.referee.command

        # commandの情報を格納するリスト
        self.__send_cmds = []
        bot: Robot
        cmd: RobotCommand

        # defenseのテスト動作
        bot = self.__observer.our_robots[2]
        cmd = self.__defensetest(bot)
        self.__send_cmds.append(cmd)

        # attack defense
        bot = self.__observer.our_robots[3]
        cmd = self.__theirdefense(bot)
        self.__send_cmds.append(cmd)

        # attack defense
        bot = self.__observer.our_robots[4]
        cmd = self.__theirdefense2(bot)
        self.__send_cmds.append(cmd)

    def __defensetest(self, robot: Robot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        distance_ball_robot = MU.distance(self.__observer.ball, robot)
        dribble_power = 0
        kickpower = 0

        # 円と直線の共有点の座標計算
        if pow(-6000 / 2, 2) <= pow((robot.x - self.__our_goal.x), 2) + pow(robot.y, 2):
            xd = self.__observer.ball.x - self.__our_goal.x
            yd = self.__observer.ball.y
            X = 0
            Y = 0
            a = xd ** 2 + yd ** 2
            b = xd * X + yd * Y
            c = X ** 2 + Y ** 2 - 3050 ** 2
            D = b ** 2 - a * c
            s1 = (-b + math.sqrt(D)) / a
            # s2 = (-b - math.sqrt(D)) / a
            target_position = Pose(self.__our_goal.x + xd * s1, yd * s1)

        elif robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
            target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
            # distance_ball_robot = distance(self.__observer.ball, robot)
            if distance_ball_robot < 150:
                dribble_power = 0
                kickpower = 3

        else:
            target_position = Pose((self.__our_goal.x + self.__observer.ball.x) / 2, self.__observer.ball.y / 2)

        radian_target_robot = MU.radian_normalize(MU.radian(target_position, robot) - robot.theta)
        distance_target_robot = MU.distance(target_position, robot)
        if distance_ball_robot > 300:
            speed = distance_target_robot / 1000
        else:
            speed = 0.5
        speed = distance_target_robot / 1000

        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_robot
        command.kickpow = kickpower
        command.dribble_pow = dribble_power
        return command

    def __defensetest2(self, robot: Robot) -> RobotCommand:  ##開発中 5/18~
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        distance_ball_robot = MU.distance(self.__observer.ball, robot)
        dribble_power = 0
        kickpower = 0

        if robot.y > (1800 * (robot.x + 6000)) / (-4200 + 6000):
            interx = (
                1800 * (self.__observer.ball.y + 6000) - 6000 * self.__observer.ball.x
            ) / self.__observer.ball.x + 0.001
            intery = -1800

        elif robot.y < -1800 * (robot.x + 6000) / (-4200 + 6000):
            interx = -4200
            intery = (self.__observer.ball.x * (-4200 + 6000)) / (self.__observer.ball.y + 6000)

        else:
            interx = (
                -1800 * (self.__observer.ball.y + 6000) - 6000 * self.__observer.ball.x
            ) / self.__observer.ball.x + 0.001
            intery = -1800
        target_position = Pose(interx, intery)
        speed = 1
        radian_target_robot = MU.radian_normalize(MU.radian(target_position, robot) - robot.theta)
        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_robot
        command.kickpow = kickpower
        command.dribble_pow = dribble_power
        return command

    def __attackdefense(self, robot: Robot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        distance_ball_robot = MU.distance(self.__observer.ball, robot)
        dribble_power = 0
        kickpower = 0

        if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
            target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
            # distance_ball_robot = distance(self.__observer.ball, robot)
            if distance_ball_robot < 150:
                dribble_power = 0
                kickpower = 3
        else:
            target_position = Pose(
                (self.__our_goal.x + 9 * self.__observer.ball.x) / 10, 9 * self.__observer.ball.y / 10
            )

        radian_target_robot = MU.radian_normalize(MU.radian(target_position, robot) - robot.theta)
        distance_target_robot = MU.distance(target_position, robot)
        if distance_ball_robot > 300:
            speed = distance_target_robot / 1000
        else:
            speed = 0.5

        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_robot
        command.kickpow = kickpower
        command.dribble_pow = dribble_power
        return command

    def __theirdefense(self, robot: Robot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        # distance_their_robot = distance(self.__observer.our_robots[0], robot)
        distance_ball_robot = MU.distance(self.__observer.ball, robot)
        dribble_power = 0
        kickpower = 0

        if pow(6000, 2) <= pow((robot.x - self.__our_goal.x), 2) + pow(robot.y, 2):
            xd = self.__observer.ball.x - self.__our_goal.x
            yd = self.__observer.ball.y
            X = 0
            Y = 0
            a = xd ** 2 + yd ** 2
            b = xd * X + yd * Y
            c = X ** 2 + Y ** 2 - 6000 ** 2
            D = b ** 2 - a * c
            s1 = (-b + math.sqrt(D)) / a
            # s2 = (-b - math.sqrt(D)) / a
            target_position = Pose(self.__our_goal.x + xd * s1, yd * s1)

        else:
            if self.__observer.ball.y < 0:
                # distance_their_robot = distance(self.__observer.our_robots[0], robot)
                if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
                    target_position = Pose(self.__observer.our_robots[1].x, self.__observer.our_robots[1].y)
                else:
                    target_position = Pose(
                        (self.__our_goal.x + self.__observer.our_robots[1].x) / 2, self.__observer.our_robots[1].y / 2
                    )
            else:
                # distance_their_robot = distance(self.__observer.our_robots[1], robot)
                # target_position = Pose(
                #    (self.__our_goal.x + 7 * self.__observer.our_robots[1].x) / 8, 7 * self.__observer.our_robots[1].y / 8
                # )
                if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
                    target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
                    # distance_ball_robot = distance(self.__observer.ball, robot)
                    if distance_ball_robot < 150:
                        dribble_power = 0
                        kickpower = 3
                else:
                    target_position = Pose(
                        (self.__our_goal.x + 9 * self.__observer.ball.x) / 10, 9 * self.__observer.ball.y / 10
                    )

        radian_target_robot = MU.radian_normalize(MU.radian(target_position, robot) - robot.theta)
        distance_target_robot = MU.distance(target_position, robot)
        if distance_ball_robot <= 300:
            speed = 0.5
        else:
            speed = distance_target_robot / 1000
        speed = distance_target_robot / 1000

        # if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
        #    target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
        #    # distance_ball_robot = distance(self.__observer.ball, robot)
        #    if distance_ball_robot < 150:
        #        dribble_power = 0
        #        kickpower = 3
        # else:

        # radian_target_robot = radian_normalize(radian(target_position, robot) - robot.theta)
        # distance_target_robot = distance(target_position, robot)
        # if distance_ball_robot > 300:
        #    speed = distance_target_robot / 1000
        # else:
        #    speed = 0.5

        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_robot
        command.kickpow = kickpower
        command.dribble_pow = dribble_power
        return command

    def __theirdefense2(self, robot: Robot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = MU.radian_normalize(MU.radian(self.__observer.ball, robot) - robot.theta)
        # distance_their_robot = distance(self.__observer.our_robots[0], robot)
        distance_ball_robot = MU.distance(self.__observer.ball, robot)
        dribble_power = 0
        kickpower = 0

        if pow(6000, 2) <= pow((robot.x - self.__our_goal.x), 2) + pow(robot.y, 2):
            xd = self.__observer.ball.x - self.__our_goal.x
            yd = self.__observer.ball.y
            X = 0
            Y = 0
            a = xd ** 2 + yd ** 2
            b = xd * X + yd * Y
            c = X ** 2 + Y ** 2 - 6000 ** 2
            D = b ** 2 - a * c
            s1 = (-b + math.sqrt(D)) / a
            # s2 = (-b - math.sqrt(D)) / a
            target_position = Pose(self.__our_goal.x + xd * s1, yd * s1)

        else:
            if self.__observer.ball.y >= 0:
                # distance_their_robot = distance(self.__observer.our_robots[0], robot)
                if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
                    target_position = Pose(self.__observer.our_robots[0].x, self.__observer.our_robots[0].y)
                else:
                    target_position = Pose(
                        (self.__our_goal.x + self.__observer.our_robots[0].x) / 2, self.__observer.our_robots[0].y / 2
                    )
            else:
                # distance_their_robot = distance(self.__observer.our_robots[1], robot)
                # target_position = Pose(
                #    (self.__our_goal.x + 7 * self.__observer.our_robots[1].x) / 8, 7 * self.__observer.our_robots[1].y / 8
                # )
                if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
                    target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
                    # distance_ball_robot = distance(self.__observer.ball, robot)
                    if distance_ball_robot < 150:
                        dribble_power = 0
                        kickpower = 3
                else:
                    target_position = Pose(
                        (self.__our_goal.x + 9 * self.__observer.ball.x) / 10, 9 * self.__observer.ball.y / 10
                    )

        radian_target_robot = MU.radian_normalize(MU.radian(target_position, robot) - robot.theta)
        distance_target_robot = MU.distance(target_position, robot)
        if distance_ball_robot <= 300:
            speed = 0.5
        else:
            speed = distance_target_robot / 1000
        # speed = distance_target_robot / 1000

        # if robot.x <= -4100 and robot.y <= 1900 and robot.y >= -1900:
        #    target_position = Pose(self.__observer.ball.x, self.__observer.ball.y)
        #    # distance_ball_robot = distance(self.__observer.ball, robot)
        #    if distance_ball_robot < 150:
        #        dribble_power = 0
        #        kickpower = 3
        # else:

        # radian_target_robot = radian_normalize(radian(target_position, robot) - robot.theta)
        # distance_target_robot = distance(target_position, robot)
        # if distance_ball_robot > 300:
        #    speed = distance_target_robot / 1000
        # else:
        #    speed = 0.5

        command.vel_fwd = math.cos(radian_target_robot) * speed
        command.vel_sway = math.sin(radian_target_robot) * speed
        command.vel_angular = radian_ball_robot
        command.kickpow = kickpower
        command.dribble_pow = dribble_power
        return command

    # def intersection(x,y):   ##function

    #   if y > 1800*(x + 6000)/(-4200 +6000):
    #      intersection_x = (1800( self._observer.ball.y +6000)/self._bserver.ball.x) - 6000
    #      intersection_y = -1800

    # elif y < -1800*(x+6000)/(-4200+6000):
    #    intersection_x = -4200
    #    intersection_y = (self._observer.ball.x*(-4200+6000))/(self._observer.ball.y + 6000)

    # else:
    #    intersection_x = (-1800( self._observer.ball.y +6000)/self._bserver.ball.x) - 6000
    #    intersection_y = -1800

    #  return intersection_x, intersection_y
