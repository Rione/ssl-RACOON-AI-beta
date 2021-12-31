#!/usr/bin/env python3.10

"""detection.py

    This module contains:
        - DetectionBall
        - DetectionRobot
        - DetectionFrame

    See also:
        https://github.com/RoboCup-SSL/ssl-vision/blob/master/src/shared/proto/messages_robocup_ssl_detection.proto
"""

from racoon_ai.models.official.vision.coordinate import Pose2D, Pose3D


class DetectionBall(Pose3D):
    """DetectionBall

    A detection of a ball.

    Args:
        confidence (float): The confidence of the detection.
        area (float): The area of the detection.
        pixel_x (int): The x-coordinate of the detection in pixels.
        pixel_y (float): The y-coordinate of the detection in pixels.
        x (float): The x-coordinate of the detection in meters.
        y (float): The y-coordinate of the detection in meters.
        z (float): The z-coordinate of the detection in meters.
    """

    def __init__(
        self,
        confidence: float,
        area: int,
        pixel_x: float,
        pixel_y: float,
        x: float,
        y: float,
        z: float,
    ):

        self.__confidence: float = confidence

        self.__area: int = area

        self.__pixel_x: float = pixel_x

        self.__pixel_y: float = pixel_y

        Pose3D.__init__(self, x, y, z=z)

    def __str__(self):
        return (
            "DetectionBall("
            f"confidence={self.confidence:.2%}, "
            f"area={self.area:d}, "
            f"pixel_x={self.pixel_x:.2f}, "
            f"pixel_y={self.pixel_y:.2f}, "
            f"x={self.x:.2f}, "
            f"y={self.y:.2f}, "
            f"theta={self.theta:.2f}, "
            f"z={self.z}"
            ")"
        )

    @property
    def confidence(self) -> float:
        """confidence

        Returns:
            float: The confidence of the detection.
        """
        return self.__confidence

    @property
    def area(self) -> int:
        """area

        Returns:
            int: The area of the detection.
        """
        return self.__area

    @property
    def pixel_x(self) -> float:
        """pixel_x

        Returns:
            float: The x-coordinate of the detection in pixels.
        """
        return self.__pixel_x

    @property
    def pixel_y(self) -> float:
        """pixel_y

        Returns:
            float: The y-coordinate of the detection in pixels.
        """
        return self.__pixel_y


class DetectionRobot(Pose2D):
    """DetectionRobot

    A detection of a robot.

    Args:
        confidence (float): The confidence of the detection.
        robot_id (int): The id of the robot.
        x (float): The x-coordinate of the robot in millimeters.
        y (float): The y-coordinate of the robot in millimeters.
        theta (float): The orientation of the robot in radians.
        pixel_x (float): The x-coordinate of the robot in pixels.
        pixel_y (float): The y-coordinate of the robot in pixels.
        height (float): The height of the robot in millimeters.
    """

    def __init__(
        self,
        confidence: float,
        robot_id: int,
        x: float,
        y: float,
        theta: float,
        pixel_x: float,
        pixel_y: float,
        height: float,
    ):

        self.__confidence: float = confidence

        self.__robot_id: int = robot_id

        self.__pixel_x: float = pixel_x

        self.__pixel_y: float = pixel_y

        self.__height: float = height

        super().__init__(x, y, theta)

    def __str__(self) -> str:
        return (
            "DetectionRobot("
            f"confidence={self.confidence:.1%}, "
            f"robot_id={self.robot_id:2d}, "
            f"x={self.x:.1f}, "
            f"y={self.y:.1f}, "
            f"theta={self.theta:.1f}, "
            f"pixel_x={self.pixel_x:.1f}, "
            f"pixel_y={self.pixel_y:.1f}, "
            f"height={self.height:.1f})"
            ")"
        )

    @property
    def confidence(self):
        """confidence

        Returns:
            float: The confidence of the detection.
        """
        return self.__confidence

    @property
    def robot_id(self) -> int:
        """robot_id

        Returns:
            int: The id of the robot.
        """
        return self.__robot_id

    @property
    def pixel_x(self) -> float:
        """pixel_x

        Returns:
            float: The x-coordinate of the robot in pixels.
        """
        return self.__pixel_x

    @property
    def pixel_y(self) -> float:
        """pixel_y

        Returns:
            float: The y-coordinate of the robot in pixels.
        """
        return self.__pixel_y

    @property
    def height(self) -> float:
        """height

        Returns:
            float: The height of the robot in millimeters.
        """
        return self.__height


class DetectionFrame:
    """DetectionFrame

    Args:
        frame_number (int): The frame number.
        t_capture (float): The time at which the frame was captured.
        t_sent (float): The time at which the frame was sent.
        camera_id (int): The camera id.
        balls (list[DetectionBall]): The list of detected balls.
        robots_yellow (list[DetectionRobot]): The list of yellow detected robots.
        robots_blue (list[DetectionRobot]): The list of blue detected robots.
    """

    def __init__(
        self,
        frame_number: int,
        t_capture: float,
        t_sent: float,
        camera_id: int,
        balls: list[DetectionBall],
        robots_yellow: list[DetectionRobot],
        robots_blue: list[DetectionRobot],
    ):

        self.__frame_number: int = frame_number

        self.__t_capture: float = t_capture

        self.__t_sent: float = t_sent

        self.__camera_id: int = camera_id

        self.__balls: list[DetectionBall] = balls

        self.__robots_yellow: list[DetectionRobot] = robots_yellow

        self.__robots_blue: list[DetectionRobot] = robots_blue

    def __str__(self):
        return (
            "DetectionFrame("
            f"frame_number={self.frame_number}, "
            f"t_capture={self.t_capture:.2f}, "
            f"t_sent={self.t_sent:.2f}, "
            f"camera_id={self.camera_id:d}, "
            f"balls={self.balls}, "
            f"robots_yellow={self.robots_yellow}, "
            f"robots_blue={self.robots_blue}"
            ")"
        )

    @property
    def frame_number(self) -> int:
        """frame_number

        Returns:
            int: The frame number.
        """
        return self.__frame_number

    @property
    def t_capture(self) -> float:
        """t_capture

        Returns:
            float: The time at which the frame was captured.
        """
        return self.__t_capture

    @property
    def t_sent(self) -> float:
        """t_sent

        Returns:
            float: The time at which the frame was sent.
        """
        return self.__t_sent

    @property
    def camera_id(self) -> int:
        """camera_id

        Returns:
            int: The id of camera.
        """
        return self.__camera_id

    @property
    def balls(self) -> list[DetectionBall]:
        """balls

        Returns:
            list[DetectionBall]: The list of detected balls.
        """
        return self.__balls

    @property
    def robots_yellow(self) -> list[DetectionRobot]:
        """robots_yellow

        Returns:
            list[DetectionRobot]: The list of yellow detected robots.
        """
        return self.__robots_yellow

    @property
    def robots_blue(self) -> list[DetectionRobot]:
        """robots_blue

        Returns:
            list[DetectionRobot]: The list of blue detected robots.
        """
        return self.__robots_blue


if __name__ == "__main__":
    dball = DetectionBall(0.9, 100, 100, 100, 0.1, 0.2, 0.3)
    print(dball)

    drobot = DetectionRobot(96, 0, 2, 4, 2, 2, 4, 20)
    print(drobot)

    dfame = DetectionFrame(1, 1.0, 1.0, 1, [dball], [drobot], [drobot])
    print(dfame)
