#!/usr/bin/env python3.10

"""replacement.py

    This module contains:
        - RobotReplacement
        - BallReplacement
        - Replacement

    See also:
        https://github.com/RoboCup-SSL/grSim/blob/master/src/proto/grSim_Replacement.proto
"""


class RobotReplacement:
    """RobotReplacement

    Attributes:
        x (float): X-coordinate of the target
        y (float): Y-coordinate of the target
        orientation (float): Direction of the target
        robot_id (int): ID of the robot
        yellow_team (bool): Whether the robot is on the yellow team
        turnon (bool): Whether the robot is turned on or not
    """

    def __init__(
        self,
        x: float,
        y: float,
        orientation: float,
        robot_id: int,
        yellow_team: bool,
        turnon: bool = False,
    ) -> None:

        self.__x: float = x

        self.__y: float = y

        self.__orientation: float = orientation

        self.__robot_id: int = robot_id

        self.__yellow_team: bool = yellow_team

        self.__turnon: bool = turnon

    def __str__(self) -> str:
        return (
            "RobotReplacement("
            f"x={self.x:.2f} ,"
            f"y={self.y:.2f} ,"
            f"dir={self.orientation:.2f} ,"
            f"id={self.robot_id:2d} ,"
            f"yellow_team={self.yellow_team!s} ,"
            f"turnon={self.turnon!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "RobotReplacement("
            f"{self.x}, "
            f"{self.y}, "
            f"{self.orientation}, "
            f"{self.robot_id}, "
            f"{self.yellow_team}, "
            f"{self.turnon}"
            ")"
        )

    @property
    def x(self) -> float:
        """x

        Returns:
            float: X-coordinate of the target
        """
        return self.__x

    @property
    def y(self) -> float:
        """y

        Returns:
            float: Y-coordinate of the target
        """
        return self.__y

    @property
    def orientation(self) -> float:
        """dir

        Returns:
            float: Direction of the target
        """
        return self.__orientation

    @property
    def robot_id(self) -> int:
        """id

        Returns:
            int: ID of the robot
        """
        return self.__robot_id

    @property
    def yellow_team(self) -> bool:
        """yellow_team

        Returns:
            bool: Whether the robot is on the yellow team
        """
        return self.__yellow_team

    @property
    def turnon(self) -> bool:
        """turnon

        Returns:
            bool: Whether the robot is turned on or not
        """
        return self.__turnon


class BallReplacement:
    """BallReplacement

    Args:
        x (float, optional): X-coordinate of the target
        y (float, optional): Y-coordinate of the target
        vx (float, optional):
        vy (float, optional):
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        vx: float = 0,
        vy: float = 0,
    ) -> None:

        self.__x: float = x

        self.__y: float = y

        self.__vx: float = vx

        self.__vy: float = vy

    def __str__(self) -> str:
        return "BallReplacement(" f"x={self.x:.2f} ," f"y={self.y:.2f} ," f"vx={self.vx:.2f} ," f"vy={self.vy:.2f}" ")"

    def __repr__(self) -> str:
        return "BallReplacement(" f"{self.x}, " f"{self.y}, " f"{self.vx}, " f"{self.vy}" ")"

    @property
    def x(self) -> float:
        """x

        Returns:
            float: X-coordinate of the target
        """
        return self.__x

    @property
    def y(self) -> float:
        """y

        Returns:
            float: Y-coordinate of the target
        """
        return self.__y

    @property
    def vx(self) -> float:
        """vx

        Returns:
            float:
        """
        return self.__vx

    @property
    def vy(self) -> float:
        """vy

        Returns:
            float:
        """
        return self.__vy


class Replacement:
    """Replacement

    Attributes:
        robot (RobotReplacement):
        ball (BallReplacement):
    """

    def __init__(
        self,
        robot: RobotReplacement,
        ball: BallReplacement,
    ) -> None:

        self.__robot: RobotReplacement = robot

        self.__ball: BallReplacement = ball

    def __str__(self) -> str:
        return f"Replacement(robot={self.robot!s}, ball={self.ball!s})"

    def __repr__(self) -> str:
        return f"Replacement({self.robot}, {self.ball})"

    @property
    def robot(self) -> RobotReplacement:
        """robot

        Returns:
            RobotReplacement: Robot replacement
        """
        return self.__robot

    @property
    def ball(self) -> BallReplacement:
        """ball

        Returns:
            BallReplacement: Ball replacement
        """
        return self.__ball
