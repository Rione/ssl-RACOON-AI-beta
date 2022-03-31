#!/usr/bin/env python3.10

"""role.py
    This module is for the Role class.
"""

from racoon_ai.common import distance
from racoon_ai.observer import Observer


class SubRole:
    """SubRole
    Args:
        vision (VisionReceiver): VisionReceiver instance.
    Attributes:
        vision (VisionReceiver): VisionReceiver instance.
        send_cmds (list[RobotCommand]): RobotCommand list.
        our_robots (list[SSL_DetectionRobot]): Our robots.
        balls (list[SSL_DetectionBall]): Balls.
    """

    def __init__(self, observer: Observer) -> None:
        self.__attacker: int = -1
        self.__receiver: int = -1
        self.__observer = observer

    def decide_sub_role(self) -> None:
        """decide_sub_role
        Returns:
            None
        """
        self.decide_attacker()
        self.decide_receiver()
        print(self.__attacker)
        print(self.__receiver)

    def decide_attacker(self) -> None:
        """decide_attacker
        Returns:
           None
        """
        attacker: list[tuple[int, float]]
        attacker = [
            (robot.robot_id, distance(self.__observer.ball, robot))
            for robot in self.__observer.our_robots
            if robot.robot_id != 0
        ]
        if attacker:
            attacker.sort(reverse=False, key=lambda x: x[1])
            self.__attacker = int(attacker[0][0])

    def decide_receiver(self) -> None:
        """decide_receiver
        Return:
          None
        """
        receiver: list[tuple[int, float]]
        receiver = [
            (robot.robot_id, distance(self.__observer.ball, self.__observer.our_robots[self.__attacker]))
            for robot in self.__observer.our_robots
            if robot.robot_id != 0
        ]
        if receiver:
            receiver.sort(reverse=False, key=lambda x: x[1])
            self.__attacker = int(receiver[0][0])
