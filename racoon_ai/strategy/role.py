#!/usr/bin/env python3.10

"""role.py

    This module is for the Role class.
"""

from logging import getLogger

from racoon_ai.networks.reciever import VisionReceiver
from racoon_ai.proto.pb_gen.ssl_vision_detection_pb2 import SSL_DetectionRobot


class Role:
    """Observer
    Args:
        vision (VisionReceiver): VisionReceiver instance.

    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self) -> None:
        self.__logger = getLogger(__name__)
        self.__logger.info("Initializing...")
        self.__our_robots: list[SSL_DetectionRobot]
        # self.__pass: int = 0
        # self.__pass_receive: int = 0
        self.__keeper: int = 0
        self.__offense: list[int] = []
        self.__defense: list[int] = []
        # self.__ball: SSL_DetectionBall
        self.__offense_quantity: int = 0
        self.__defence_quantity: int = 0

    def vision_receive(self, vision: VisionReceiver) -> None:
        """vision_receive
        racoon_ai/strategy/role.py:35:8: W0238: Unused private member `Role.__defence` (unused-private-member)

                vision情報の受け取り
                Returns:
                    None
        """
        self.__our_robots = vision.blue_robots
        # self.__ball = vision.get_ball()

    def decide_keeper(self) -> None:
        """decide_keeper

        キーパーの決定を行います
        Returns:
            None
        """
        self.__keeper = 0

    def decide_role(self) -> None:
        """decide_role
          ロールの決定を行います
        Returns:
            None
        """
        self.decide_keeper()

        self.__offense_quantity = 3
        self.__defence_quantity = 3

        self.decide_defense()
        self.decide_offense()
        print(self.__keeper)
        print(self.__offense)
        print(self.__defense)

    def decide_defense(self) -> None:
        """decide_defense

        defenseの決定を行います
        Returns:
            None
        """

        defense: list[list[float]] = []
        for robot in self.__our_robots:
            if robot.robot_id != self.__keeper:
                defense.append([robot.robot_id, robot.x, robot.y])
        defense.sort(reverse=False, key=lambda x: x[1])
        defense = defense[: self.__defence_quantity]
        defense.sort(reverse=True, key=lambda x: x[2])
        self.__defense = [int(row[0]) for row in defense]

    def decide_offense(self) -> None:
        """decide_offense

        オフェンスの決定を行います
        Returns:
            None
        """

        offense: list[list[float]] = []
        for robot in self.__our_robots:
            if robot.robot_id != self.__keeper and robot.robot_id not in self.__defense:
                offense.append([robot.robot_id, robot.x, robot.y])
        offense.sort(reverse=True, key=lambda x: x[1])
        offense = offense[: self.__offense_quantity]
        offense.sort(reverse=True, key=lambda x: x[2])
        self.__offense = [int(row[0]) for row in offense]
