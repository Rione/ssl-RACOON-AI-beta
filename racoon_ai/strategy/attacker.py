#!/usr/bin/env python3.10

"""attacker.py

    This module is for the Attacker class.
"""

import math
from typing import Any, TypeAlias

from racoon_ai.models.coordinate import Point
from racoon_ai.models.robot.commands import RobotCommand, SimCommands
from racoon_ai.networks.vision_receiver import VisionReceiver
from racoon_ai.observer.observer import Observer
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionBall, SSL_DetectionRobot

RadFactors: TypeAlias = Point | SSL_DetectionBall | SSL_DetectionRobot


def radian(object1: RadFactors, object2: RadFactors) -> float:
    """radian

    Args:
        object1 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.
        object2 (Point | SSL_DetectionBall | SSL_DetectionRobot): Calculatable object.

    Returns:
        float: degree of two objects in radian
    """
    return math.atan2(object1.y - object2.y, object1.x - object2.x)


def radian_normalize(rad: float) -> float:
    """radian_normalize

    Args:
        rad (float): radian value

    Returns:
        float: normalized radian value
    """
    if rad > math.pi:
        rad = rad - 2 * math.pi
    if rad < -math.pi:
        rad = rad + 2 * math.pi

    return rad


def distance(object1: RadFactors, object2: RadFactors) -> float:
    """distance

    Returns:
        float: distance value
    """
    return math.sqrt(math.pow(object1.x - object2.x, 2) + math.pow(object1.y - object2.y, 2))


class Attacker(object):
    """Attacker
    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self, observer: Observer, role: Any):
        self.__observer = observer
        self.__role: Any = role
        self.__send_cmds: list[RobotCommand]
        self.__our_robots: list[SSL_DetectionRobot]
        self.__ball: SSL_DetectionBall
        self.__their_robots: list[SSL_DetectionRobot]
        self.__kick_flag: bool = False
        self.__arrive_flag: bool = False

    @property
    def send_cmds(self) -> list[RobotCommand]:
        """send_cmds

        Returns:
            list[RobotCommand]: send_cmds
        """
        return self.__send_cmds

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive

        Returns:
            None
        """
        self.__our_robots = vision.blue_robots
        self.__ball = vision.ball
        self.__their_robots = vision.yellow_robots

    def main(self) -> SimCommands:
        """main

        Returns:
            None
        """
        commands = SimCommands()
        for robot in self.__our_robots:
            if robot.robot_id >= 2:
                break
            elif robot.robot_id == self.__role.get_pass() and self.__kick_flag is False:
                distance_ball_robot = distance(robot, self.__ball)
                radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
                if distance_ball_robot < 123 and abs(math.degrees(radian_ball_robot)) < 15:
                    goal_position = Point(6000, 0, 0)
                    distance_goal_robot = distance(goal_position, robot)
                    if distance_goal_robot < 4500:
                        self.__arrive_flag = True
                        command = self._kick_ball(robot, goal_position)
                    else:
                        command = self._kick_ball(robot, self.__our_robots[self.__role.get_pass_receive()])
                else:
                    command = self._wrap_calc(robot)
            elif robot.robot_id == self.__role.get_pass() and self.__kick_flag is True:
                if robot.robot_id == 1:
                    target_position = Point(
                        self.__ball.x + 1821.0,
                        self.__ball.y - 2121.0,
                        0,
                    )
                else:
                    target_position = Point(
                        self.__ball.x + 1800.0,
                        self.__ball.y + 2121.0,
                        0,
                    )
                if (
                    abs(abs(target_position.x) - abs(self.__our_robots[self.__role.get_pass_receive()].x)) < 150
                    and abs(abs(target_position.y) - abs(self.__our_robots[self.__role.get_pass_receive()].y)) < 150
                ):
                    self.__arrive_flag = True
                else:
                    self.__arrive_flag = False

                command = self._move_point(robot, self.__ball, target_position)
            else:
                if self.__kick_flag is True:
                    command = self._pass_receive(robot)
                else:
                    if robot.robot_id == 1:
                        target_position = Point(
                            self.__ball.x + 1800.0,
                            self.__ball.y - 2121.0,
                            0,
                        )
                    else:
                        target_position = Point(
                            self.__ball.x + 1800.0,
                            self.__ball.y + 2121.0,
                            0,
                        )
                    if (
                        abs(abs(target_position.x) - abs(self.__our_robots[self.__role.get_pass_receive()].x)) < 150
                        and abs(abs(target_position.y) - abs(self.__our_robots[self.__role.get_pass_receive()].y)) < 150
                    ):
                        self.__arrive_flag = True
                    else:
                        self.__arrive_flag = False

                    command = self._move_point(robot, self.__ball, target_position)
            command = self._wrap_calc(robot)
            command = self._avoid_collision(robot, command)
            commands.robot_commands.append(command)
        return commands

    def _wrap_aroud(self, robot: SSL_DetectionRobot) -> RobotCommand:
        const = 90

        target = Point(6000, 0, 0)
        radian_ball_robot = radian(self.__ball, robot)
        radian_target_ball = radian(target, self.__ball)
        radian_target_robot = radian(target, robot)
        radian_robot_ball = radian(robot, self.__ball)
        distance_ball_robot = distance(robot, self.__ball)

        angular = radian_normalize(radian_target_robot - robot.orientation)

        radian_around = 0.0
        if radian_ball_robot - radian_target_ball != 0.0:
            radian_around = radian_ball_robot - math.pi / 2.0 * (
                radian_normalize(radian_robot_ball - radian_target_ball)
                / abs(radian_normalize(radian_robot_ball - radian_target_ball))
            )
        surge = abs(radian_target_robot - radian_ball_robot) / distance_ball_robot / 2.0 * math.cos(
            radian_around - robot.orientation
        ) + (distance_ball_robot - const) / 0.3 * abs(distance_ball_robot - const) * math.cos(
            radian_ball_robot - robot.orientation
        )
        sway = abs(radian_target_robot - radian_ball_robot) / distance_ball_robot / 2.0 * math.sin(
            radian_around - robot.orientation
        ) + (distance_ball_robot - const) / 0.3 * abs(distance_ball_robot - const) * math.sin(
            radian_ball_robot - robot.orientation
        )

        if radian_target_robot - radian_ball_robot != 0:
            speed = 0.40 / math.pow(radian_target_robot - radian_ball_robot, 2)
            surge += speed * math.cos(radian_target_robot - robot.orientation)
            sway += speed * math.sin(radian_target_robot - robot.orientation)

        adjustment = math.sqrt(surge * surge + sway * sway)
        if adjustment > 1:
            surge /= adjustment
            sway /= adjustment

        command = RobotCommand(robot.robot_id)
        command.vel_fwd = surge
        command.vel_sway = sway
        command.vel_angular = angular
        print(radian_around)
        return command

    def _wrap_calc(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        distance_ball = distance(self.__ball, robot)
        _radian = radian_normalize(radian(self.__ball, robot) - robot.orientation)

        a_constant = -0.001902256
        b_constant = 2.047918685
        c_constant = -1.932145886

        degree = math.degrees(_radian)
        if degree < 0:
            degree = abs(degree)
            wrap_degree = -(degree * degree * a_constant + degree * b_constant + c_constant - 360.0)
        else:
            wrap_degree = degree * degree * a_constant + degree * b_constant + c_constant
        if wrap_degree > 180:
            wrap_degree = wrap_degree - 360
        wrap_radian = math.radians(wrap_degree)

        if distance_ball > 1000:
            wrap_radian = _radian

        speed = distance_ball / 1000.0
        if speed > 1:
            speed = 1.0
        command.vel_fwd = math.cos(wrap_radian) * speed
        command.vel_sway = math.sin(wrap_radian) * speed
        command.vel_angular = -robot.orientation * 2.0
        command.kickpow = 0
        command.dribble_pow = 0
        return command

    def _pass_receive(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        target_position = Point(0, 0, 0)
        distance_ball_robot = distance(robot, self.__ball)
        print(self.__observer.get_ball_slope())
        if distance_ball_robot < 250:
            self.__kick_flag = False

        if self.__kick_flag is True and self.__observer.get_ball_slope() != 0:
            target_position.x = (
                robot.y - self.__observer.get_ball_intercept() - (-1 / self.__observer.get_ball_slope()) * robot.x
            ) / (self.__observer.get_ball_slope() - (-1 / self.__observer.get_ball_slope()))
            target_position.y = (
                self.__observer.get_ball_slope() * target_position.x + self.__observer.get_ball_intercept()
            )
        angular = radian_normalize(radian(self.__ball, robot) - robot.orientation)

        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_target_robot = distance(target_position, robot)
        speed = distance_target_robot / 1000
        if speed > 1:
            speed = 1
        fwd = math.cos(radian_target_robot) * speed * 2
        sway = math.sin(radian_target_robot) * speed * 2

        command.vel_fwd = fwd
        command.vel_sway = sway
        command.vel_angular = angular

        return command

    def _move_point(
        self, robot: SSL_DetectionRobot, angular_target: RadFactors, target_position: RadFactors
    ) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_angular_target_robot = radian_normalize(radian(angular_target, robot) - robot.orientation)
        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_target_robot = distance(target_position, robot) / 1000
        if distance_target_robot >= 1:
            distance_target_robot = 1

        command.kickpow = 0
        command.vel_fwd = math.cos(radian_target_robot) * distance_target_robot
        command.vel_sway = math.sin(radian_target_robot) * distance_target_robot
        command.vel_angular = radian_angular_target_robot
        return command

    def _straight_move_ball(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        distance_target_robot = distance(self.__ball, robot) / 1000
        if distance_target_robot >= 1:
            distance_target_robot = 1

        command.kickpow = 0
        command.vel_fwd = math.cos(radian_ball_robot) * distance_target_robot
        command.vel_sway = math.sin(radian_ball_robot) * distance_target_robot
        command.vel_angular = radian_ball_robot * 2
        command.dribble_pow = 0
        return command

    def _kick_ball(self, robot: SSL_DetectionRobot, target_position: RadFactors) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_ball_robot = distance(self.__ball, robot)
        speed_limit = distance_ball_robot / 1000.0
        if speed_limit >= 1.0:
            speed_limit = 1.0

        angular = radian_target_robot

        kick_power = 0
        if abs(math.degrees(radian_target_robot)) < 5 and self.__arrive_flag is True:
            kick_power = 3
            self.__kick_flag = True

        command.vel_fwd = math.cos(radian_ball_robot) * speed_limit
        command.vel_sway = math.sin(radian_ball_robot) * speed_limit
        command.vel_angular = angular * 2
        command.kickpow = kick_power
        command.dribble_pow = 1
        return command

    def _avoid_collision(self, robot: SSL_DetectionRobot, command: RobotCommand) -> RobotCommand:
        if self.__observer.get_ball_slope() == 0:
            self.__kick_flag = False
        nearest_robot, min_distance = self._det_near_robot(robot)
        if min_distance < 300:
            degree_invasion = radian(self.__their_robots[nearest_robot], robot) - robot.orientation
            if degree_invasion > 0:
                avoid_degree = degree_invasion + math.pi / 2
                command.vel_fwd = math.cos(avoid_degree)
                command.vel_sway = math.sin(avoid_degree)
            else:
                avoid_degree = degree_invasion - math.pi / 2
                command.vel_fwd = math.cos(avoid_degree - math.pi)
                command.vel_sway = math.sin(avoid_degree - math.pi)

        return command

    def _det_near_robot(self, robot: SSL_DetectionRobot) -> tuple[int, float]:
        min_robot_id = -1
        min_distance = 10000000.0
        for their_count in range(5):
            dist = distance(self.__their_robots[their_count], robot)
            if dist < min_distance:
                min_distance = dist
                min_robot_id = their_count
        return min_robot_id, min_distance

        # robot_difference_x = self.__pre_robots[robot.robot_id].x - robot.x
        # robot_difference_y = self.__pre_robots[robot.robot_id].y - robot.y

        # robot_speed = []
        # robot_speed[robot.robot_id] = math.sqrt(pow(robot_difference_x, 2) + pow(robot_difference_y, 2)) / 0.016

        # self.__pre_robots[robot.robot_id] = robot

    def get_kick_flag(self) -> bool:
        """
        Returns:
            bool: __kick_flag
        """
        return self.__kick_flag
