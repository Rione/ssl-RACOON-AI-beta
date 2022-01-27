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

    def _stop(self, id1: int, id2: int, commands: SimCommands) -> None:
        command1 = RobotCommand(id1)
        command1.vel_fwd = 0
        command1.vel_sway = 0
        command1.vel_angular = 0
        command1.kickpow = 0
        command1.dribble_pow = 0

        command2 = RobotCommand(id2)
        command2.vel_fwd = 0
        command2.vel_sway = 0
        command2.vel_angular = 0
        command2.kickpow = 0
        command2.dribble_pow = 0

        commands.robot_commands.append(command1)
        if command1 != command2:
            commands.robot_commands.append(command2)

    def main(self) -> SimCommands:
        """main

        Returns:
            None
        """
        commands = SimCommands()
        target_radian = 0.0
        if len(self.__our_robots) == 0:
            self._stop(0, 1, commands)
        elif len(self.__our_robots) == 1:
            for robot in self.__our_robots:
                if robot.robot_id == 0:
                    self._stop(1, 1, commands)
                elif robot.robot_id == 1:
                    self._stop(0, 0, commands)

        for robot in self.__our_robots:
            goal_position = Point(-1400, 0, 0)
            # print(math.degrees(radian_normalize(radian(self.__ball, robot) - robot.orientation)))
            if robot.robot_id >= 2:
                break
            elif robot.robot_id == self.__role.get_pass() and self.__kick_flag is False:
                # print(self.__status.get_infrared(0))
                # if self.__status.get_infrared(0) is True:
                distance_ball = distance(self.__ball, robot)
                _radian = radian_normalize(radian(self.__ball, robot) - robot.orientation)
                goal_position = Point(-1400, 0, 0)
                distance_goal_robot = distance(goal_position, self.__ball)
                if distance_ball < 110 and abs(math.degrees(_radian)) < 8:
                    if distance_goal_robot < 1150:
                        self.__arrive_flag = True
                        command = self._kick_ball(robot, goal_position)
                    else:
                        command = self._kick_ball(robot, self.__our_robots[self.__role.get_pass_receive()])
                else:
                    if distance_goal_robot < 1150:
                        command = self._wrap_calc(robot, goal_position)
                    else:
                        command = self._wrap_calc(robot, self.__our_robots[self.__role.get_pass_receive()])
            elif robot.robot_id == self.__role.get_pass() and self.__kick_flag is True:
                if robot.robot_id == 1:
                    target_position = Point(
                        300,
                        -700,
                        0,
                    )
                else:
                    target_position = Point(
                        -800,
                        600,
                        0,
                    )
                if (
                    abs(abs(target_position.x) - abs(self.__our_robots[self.__role.get_pass_receive()].x)) < 150
                    and abs(abs(target_position.y) - abs(self.__our_robots[self.__role.get_pass_receive()].y)) < 150
                ):
                    self.__arrive_flag = True
                else:
                    self.__arrive_flag = False

                command, target_radian = self._move_point(robot, self.__ball, target_position)
            else:
                if self.__kick_flag is True:
                    command = self._pass_receive(robot)
                else:
                    if robot.robot_id == 1:
                        target_position = Point(
                            300,
                            -700,
                            0,
                        )
                    else:
                        target_position = Point(
                            -800,
                            600,
                            0,
                        )
                    if (
                        abs(abs(target_position.x) - abs(self.__our_robots[self.__role.get_pass_receive()].x)) < 150
                        and abs(abs(target_position.y) - abs(self.__our_robots[self.__role.get_pass_receive()].y)) < 150
                    ):
                        self.__arrive_flag = True
                    else:
                        self.__arrive_flag = False

                    command, target_radian = self._move_point(robot, self.__ball, target_position)
            command = self._avoid_collision(robot, command, target_radian)
            # command = self._wrap_calc(robot)
            if self.__ball.x == 0.0:
                self._stop(0, 1, commands)
            else:
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

    def _wrap_calc(self, robot: SSL_DetectionRobot, target: RadFactors) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        distance_ball = distance(self.__ball, robot)
        _radian = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        radian_target_robot = radian_normalize(radian(target, robot) - robot.orientation)

        a_constant = -0.001902256
        b_constant = 2.307918685
        c_constant = -1.932145886

        degree = math.degrees(_radian)
        degree = degree - 2.0
        if degree < 0:
            degree = abs(degree)
            wrap_degree = -(degree * degree * a_constant + degree * b_constant + c_constant - 360.0)
        else:
            wrap_degree = degree * degree * a_constant + degree * b_constant + c_constant
        if wrap_degree > 180:
            wrap_degree = wrap_degree - 360
        wrap_radian = math.radians(wrap_degree)

        if distance_ball > 500:
            wrap_radian = _radian

        speed = distance_ball / 1000.0
        if speed > 0.25:
            speed = 0.25
        elif speed < 0.13:
            speed = 0.13

        # speed = 0
        if target.x == -1400:
            angular = 0.08
        else:
            angular = 0.12
        command.vel_fwd = math.cos(wrap_radian) * speed
        command.vel_sway = math.sin(wrap_radian) * speed
        command.vel_angular = radian_target_robot * angular
        command.kickpow = 0
        command.dribble_pow = 0
        return command

    def _pass_receive(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        target_position = Point(0, 0, 0)
        distance_ball_robot = distance(robot, self.__ball)
        # print(self.__observer.get_ball_slope())
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
        if speed > 0.3:
            speed = 0.3
        elif speed < 0.18:
            speed = 0.18
        fwd = math.cos(radian_target_robot) * speed
        sway = math.sin(radian_target_robot) * speed

        command.vel_fwd = fwd
        command.vel_sway = sway
        command.vel_angular = angular * 0.12
        command.dribble_pow = 1

        return command

    def _move_point(
        self, robot: SSL_DetectionRobot, angular_target: RadFactors, target_position: RadFactors
    ) -> tuple[RobotCommand, float]:
        command = RobotCommand(robot.robot_id)
        radian_angular_target_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_target_robot = distance(target_position, robot) / 1000
        if distance_target_robot >= 0.3:
            distance_target_robot = 0.3
        angular_target.x = 10
        command.kickpow = 0
        command.vel_fwd = math.cos(radian_target_robot) * distance_target_robot
        command.vel_sway = math.sin(radian_target_robot) * distance_target_robot
        command.vel_angular = radian_angular_target_robot * 0.12
        return command, radian_target_robot

    def _straight_move_ball(self, robot: SSL_DetectionRobot) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        distance_target_robot = distance(self.__ball, robot) / 1000
        if distance_target_robot >= 0.2:
            distance_target_robot = 0.2

        command.kickpow = 0
        command.vel_fwd = math.cos(radian_ball_robot) * distance_target_robot
        command.vel_sway = math.sin(radian_ball_robot) * distance_target_robot
        command.vel_angular = radian_ball_robot * 0.1
        command.dribble_pow = 0
        return command

    def _kick_ball(self, robot: SSL_DetectionRobot, target_position: RadFactors) -> RobotCommand:
        command = RobotCommand(robot.robot_id)
        radian_ball_robot = radian_normalize(radian(self.__ball, robot) - robot.orientation)
        radian_target_robot = radian_normalize(radian(target_position, robot) - robot.orientation)
        distance_ball_robot = distance(self.__ball, robot)
        speed_limit = distance_ball_robot / 1000.0
        if speed_limit >= 0.15:
            speed_limit = 0.15

        angular = radian_target_robot

        kick_power = 0.0
        # if abs(math.degrees(radian_target_robot)) < 10 and self.__arrive_flag is True:
        if abs(math.degrees(radian_target_robot)) < 8 and self.__arrive_flag is True:
            if target_position.x == -1400:
                kick_power = 10.0
                self.__kick_flag = True
            else:
                if robot.robot_id == 1:
                    kick_power = 1.05
                    self.__kick_flag = True
                else:
                    kick_power = 0.85
                    self.__kick_flag = True

        spin = angular * 0.12
        if spin > 0:
            spin = 0.03
        else:
            spin = -0.03

        command.vel_fwd = math.cos(radian_ball_robot) * speed_limit
        command.vel_sway = math.sin(radian_ball_robot) * speed_limit
        command.vel_angular = spin
        command.kickpow = kick_power
        command.dribble_pow = 1
        return command

    def _avoid_collision(self, robot: SSL_DetectionRobot, command: RobotCommand, target_radian: float) -> RobotCommand:
        if self.__observer.get_ball_slope() == 0:
            self.__kick_flag = False
        nearest_robot, min_distance, min_radian = self._det_near_robot(robot)
        # if robot.robot_id == 0:
        #    print(min_radian, target_radian)
        if min_distance < 380 and ((min_radian > 0 and target_radian > 0) or (min_radian < 0 and target_radian < 0)):
            for robot_their in range(4):
                if self.__their_robots[robot_their].robot_id == nearest_robot:
                    degree_invasion = radian(self.__their_robots[robot_their], robot) - robot.orientation
                    if degree_invasion > 0:
                        avoid_degree = degree_invasion + math.pi / 2
                        command.vel_fwd = math.cos(avoid_degree) * 0.25
                        command.vel_sway = math.sin(avoid_degree) * 0.25
                    else:
                        avoid_degree = degree_invasion - math.pi / 2
                        command.vel_fwd = math.cos(avoid_degree - math.pi) * 0.25
                        command.vel_sway = math.sin(avoid_degree - math.pi) * 0.25

        return command

    def _det_near_robot(self, robot: SSL_DetectionRobot) -> tuple[int, float, float]:
        min_robot_id = -1
        min_distance = 10000000.0
        min_radian = 0.0
        for robot_their in range(4):
            if robot.robot_id == 0 and self.__their_robots[robot_their].robot_id == 3:
                min_robot_id = 3
                min_radian = radian_normalize(radian(self.__their_robots[robot_their], robot) - robot.orientation)
                min_distance = distance(self.__their_robots[robot_their], robot)
            elif robot.robot_id == 1 and self.__their_robots[robot_their].robot_id == 4:
                min_robot_id = 4
                min_radian = radian_normalize(radian(self.__their_robots[robot_their], robot) - robot.orientation)
                min_distance = distance(self.__their_robots[robot_their], robot)

        # print(self.__their_robots)
        # for robot_their in range(4):
        #     dist = distance(self.__their_robots[robot_their], robot)
        #     if dist < min_distance:
        #         if self.__their_robots[robot_their].robot_id == 3 or self.__their_robots[robot_their].robot_id == 4:
        #             min_radian = radian_normalize(radian(self.__their_robots[0], robot) - robot.orientation)
        #             min_distance = dist
        #             min_robot_id = self.__their_robots[robot_their].robot_id
        return min_robot_id, min_distance, min_radian

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
