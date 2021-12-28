#!/usr/bin/env python3.10

"""detection_tracker.py

    This module contains:
        - Vector
        - Vector2f
        - Vector3f
        - Capability
        - TrackedBall
        - KickedBall
        - TrackedRobot
        - TrackedFrame

    See also:
        https://github.com/RoboCup-SSL/ssl-vision/blob/master/src/shared/proto/messages_robocup_ssl_detection_tracked.proto
"""

from enum import Enum
from models.official.game_controller.common import Team, RobotId


class Vector:
    """Vector

    DO NOT USE THIS CLASS DIRECTLY.
    This is a base class for 2D and 3D vectors.
    """

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(
                f"Cannot compare {type(self).__name__} to {type(other).__name__}"
            )
        return self.__dict__ == other.__dict__

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(
                f"Cannot compare {type(self).__name__} to {type(other).__name__}"
            )
        return not self.__eq__(other)

    def __abs__(self) -> float:
        raise NotImplementedError

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Cannot compare {type(self)} to {type(other)}")
        return abs(self) < abs(other)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Cannot compare {type(self)} to {type(other)}")
        return abs(self) <= abs(other)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Canot compare {type(self)} to {type(other)}")
        return abs(self) <= abs(other)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            raise TypeError(f"Canot compare {type(self)} to {type(other)}")
        return abs(self) <= abs(other)


class Vector2f(Vector):
    """Vector2f

    Attributes:
        x (float): x axis value
        y (float): y axis value
    """

    def __init__(self, x: float, y: float) -> None:
        self.__x: float = x
        self.__y: float = y

    def __str__(self) -> str:
        return f"Vector2f(x={self.x:.2f}, y={self.y:.2f})"

    def __repr__(self) -> str:
        return f"Vector2f(x={self.x}, y={self.y})"

    def __iadd__(self, other: object) -> "Vector2f":
        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for '{type(self)}' and '{type(other)}'"
            )
        self.__x += other.x
        self.__y += other.y
        return self

    def __isub__(self, other: object) -> "Vector2f":
        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for '{type(self)}' and '{type(other)}'"
            )
        self.__x -= other.x
        self.__y -= other.y
        return self

    def __add__(self, other: object) -> "Vector2f":
        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for '{type(self)}' and '{type(other)}'"
            )
        return Vector2f(self.x + other.x, self.y + other.y)

    def __sub__(self, other: object) -> "Vector2f":
        if not isinstance(other, type(self)):
            raise TypeError(
                f"unsupported operand type(s) for '{type(self)}' and '{type(other)}'"
            )
        return Vector2f(self.x - other.x, self.y - other.y)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    @property
    def x(self) -> float:
        """x

        Returns:
            float: x value
        """
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        """x

        Args:
            value (float): x value
        """
        self.__x = value

    @property
    def y(self) -> float:
        """y

        Returns:
            float: y value
        """
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        """y

        Args:
            value (float): y value
        """
        self.__y = value


class Vector3f(Vector):
    """Vector3f

    Attributes:
        x (float): x axis value
        y (float): y axis value
        z (float): z axis value
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.__x: float = x
        self.__y: float = y
        self.__z: float = z

    def __str__(self) -> str:
        return f"Vector3f(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"

    def __repr__(self) -> str:
        return f"Vector3f({self.x}, {self.y}, {self.z})"

    def __iadd__(self, other: "Vector3f") -> "Vector3f":
        self.__x += other.x
        self.__y += other.y
        self.__z += other.z
        return self

    def __isub__(self, other: "Vector3f") -> "Vector3f":
        self.__x -= other.x
        self.__y -= other.y
        self.__z -= other.z
        return self

    def __add__(self, other: "Vector3f") -> "Vector3f":
        return Vector3f(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3f") -> "Vector3f":
        return Vector3f(self.x - other.x, self.y - other.y, self.z - other.z)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    @property
    def x(self) -> float:
        """x

        Returns:
            float: x value
        """
        return self.__x

    @x.setter
    def x(self, value: float) -> None:
        """x

        Args:
            value (float): x value
        """
        self.__x = value

    @property
    def y(self) -> float:
        """y

        Returns:
            float: y value
        """
        return self.__y

    @y.setter
    def y(self, value: float) -> None:
        """y

        Args:
            value (float): y value
        """
        self.__y = value

    @property
    def z(self) -> float:
        """z

        Returns:
            float: z value
        """
        return self.__z

    @z.setter
    def z(self, value: float) -> None:
        """z

        Args:
            value (float): z value
        """
        self.__z = value


class Capability(Enum):
    """Capability

    Capabilities that a source implementation can have.
    """

    CAPABILITY_UNKNOWN = 0

    CAPABILITY_DETECT_FLYING_BALLS = 1

    CAPABILITY_DETECT_MULTIPLE_BALLS = 2

    CAPABILITY_DETECT_KICKED_BALLS = 3


class TrackedBall:
    """TrackedBall

    A single tracked ball.

    Attributes:
        pos (Vector3f):
            The position (x, y, height) [m] in the ssl-vision coordinate system
        vel (Vector3f, optional):
            The velocity [m/s] in the ssl-vision coordinate system
        visibility (float, optional):
            The visibility of the ball
            A value between 0 (not visible) and 1 (visible)
            The exact implementation depends on the source software
            -1 if not set
    """

    def __init__(
        self,
        pos: Vector3f,
        vel: Vector3f = Vector3f(0, 0, 0),
        visibility: float = -1,
    ) -> None:

        self.__pos: Vector3f = pos

        self.__vel: Vector3f = vel

        self.__visibility: float = visibility

    def __str__(self) -> str:
        return (
            "TrackedBall("
            f"pos={self.pos!s}, "
            f"vel={self.vel!s}, "
            f"visibility={self.visibility:.1%}"
            ")"
        )

    def __repr__(self) -> str:
        return f"TrackedBall({self.pos}, {self.vel}, {self.visibility})"

    @property
    def pos(self) -> Vector3f:
        """pos

        Returns:
            Vector3f: position
        """
        return self.__pos

    @property
    def vel(self) -> Vector3f:
        """vel

        Returns:
            Vector3f: velocity
        """
        return self.__vel

    @property
    def visibility(self) -> float:
        """visibility

        Returns:
            float: visibility
        """
        return self.__visibility


class KickedBall:
    """KickedBall

    A ball kicked by a robot, including predictions when the ball will come to a stop

    Attributes:
        pos (Vector2f):
            The initial position [m] from which the ball was kicked
        vel (Vector3f):
            The initial velocity [m/s] with which the ball was kicked
        start_timestamp (float):
            The unix timestamp [s] when the kick was performed
        stop_timestamp (float, optional):
            The predicted unix timestamp [s] when the ball comes to a stop
        stop_pos (Vector2f, optional):
            The predicted position [m] at which the ball will come to a stop
        robot_id (RobotId, optional):
            The robot that kicked the ball
    """

    def __init__(
        self,
        pos: Vector2f,
        vel: Vector3f,
        start_timestamp: float,
        stop_timestamp: float = 0,
        stop_pos: Vector2f = Vector2f(0, 0),
        robot_id: RobotId = RobotId(-1, Team.UNKNOWN),
    ) -> None:

        self.__pos: Vector2f = pos

        self.__vel: Vector3f = vel

        self.__start_timestamp: float = start_timestamp

        self.__stop_timestamp: float = stop_timestamp

        self.__stop_pos: Vector2f = stop_pos

        self.__robot_id: RobotId = robot_id

    def __str__(self) -> str:
        return (
            "KickedBall("
            f"pos={self.pos!s}, "
            f"vel={self.vel!s}, "
            f"start_timestamp={self.start_timestamp:.3f}, "
            f"stop_timestamp={self.stop_timestamp:.3f}, "
            f"stop_pos={self.stop_pos!s}, "
            f"robot_id={self.robot_id!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "KickedBall("
            f"{self.pos}, "
            f"{self.vel}, "
            f"{self.start_timestamp}, "
            f"{self.stop_timestamp}, "
            f"{self.stop_pos}, "
            f"{self.robot_id}"
            ")"
        )

    @property
    def pos(self) -> Vector2f:
        """pos

        Returns:
            Vector2f: position
        """
        return self.__pos

    @property
    def vel(self) -> Vector3f:
        """vel

        Returns:
            Vector3f: velocity
        """
        return self.__vel

    @property
    def start_timestamp(self) -> float:
        """start_timestamp

        Returns:
            float: start timestamp
        """
        return self.__start_timestamp

    @property
    def stop_timestamp(self) -> float:
        """stop_timestamp

        Returns:
            float: stop timestamp
        """
        return self.__stop_timestamp

    @property
    def stop_pos(self) -> Vector2f:
        """stop_pos

        Returns:
            Vector2f: stop position
        """
        return self.__stop_pos

    @property
    def robot_id(self) -> RobotId:
        """robot_id

        Returns:
            RobotId: robot id
        """
        return self.__robot_id


class TrackedRobot:
    """TrackedRobot

    A single tracked robot.

    Attributes:
        robot_id (RobotId):
            The robot id
        pos (Vector2f):
            The position [m] in the ssl-vision coordinate system
        orientation (float):
            The orientation [rad] in the ssl-vision coordinate system
        vel (Vector2f, optional):
            The velocity [m/s] in the ssl-vision coordinate system
        vel_angular (float, optional):
            The angular velocity [rad/s] in the ssl-vision coordinate system
        visibility (float, optional):
            The visibility of the robot
            A value between 0 (not visible) and 1 (visible)
            The exact implementation depends on the source software
    """

    def __init__(
        self,
        robot_id: RobotId,
        pos: Vector2f,
        orientation: float,
        vel: Vector2f = Vector2f(0, 0),
        vel_angular: float = 0,
        visibility: float = -1,
    ) -> None:

        self.__robot_id: RobotId = robot_id

        self.__pos: Vector2f = pos

        self.__orientation: float = orientation

        self.__vel: Vector2f = vel

        self.__vel_angular: float = vel_angular

        self.__visibility: float = visibility

    def __str__(self) -> str:
        return (
            "TrackedRobot("
            f"robot_id={self.robot_id!s}, "
            f"pos={self.pos!s}, "
            f"orientation={self.orientation:.1f}, "
            f"vel={self.vel!s}, "
            f"vel_angular={self.vel_angular:.1f}, "
            f"visibility={self.visibility:.1%}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "TrackedRobot("
            f"{self.robot_id}, "
            f"{self.pos}, "
            f"{self.orientation}, "
            f"{self.vel}, "
            f"{self.vel_angular}, "
            f"{self.visibility}"
            ")"
        )

    @property
    def robot_id(self) -> RobotId:
        """robot_id

        Returns:
            RobotId: robot id
        """
        return self.__robot_id

    @property
    def pos(self) -> Vector2f:
        """pos

        Returns:
            Vector2f: position
        """
        return self.__pos

    @property
    def orientation(self) -> float:
        """orientation

        Returns:
            float: orientation
        """
        return self.__orientation

    @property
    def vel(self) -> Vector2f:
        """vel

        Returns:
            Vector2f: velocity
        """
        return self.__vel

    @property
    def vel_angular(self) -> float:
        """vel_angular

        Returns:
            float: angular velocity
        """
        return self.__vel_angular

    @property
    def visibility(self) -> float:
        """visibility

        Returns:
            float: visibility
        """
        return self.__visibility


class TrackedFrame:
    """TrackedFrame

    A frame that contains all currently tracked objects on the field on all cameras

    Attributes:
        frame_number (int):
            A monotonous increasing frame counter
        timestamp (float):
            The unix timestamp in [s] of the data
        balls (List[TrackedBall]):
            The list of detected balls
            The first ball is the primary one
            Sources may add additional balls based on their capabilities
        robots (List[TrackedRobot]):
            The list of detected robots of the both teams
        kicked_ball (KickedBall, optional):
            Information about a kicked ball, if the ball was kicked by a robot
            and is still moving
            Note: This field is optional. Some source implementations mightnot set
        capabilties (List[str], optional):
            List of capabilities of the source implementation
    """

    def __init__(
        self,
        frame_number: int,
        timestamp: float,
        balls: list[TrackedBall],
        robots: list[TrackedRobot],
        kicked_ball: KickedBall,
        capabilities: list[Capability],
    ) -> None:

        self.__frame_number: int = frame_number

        self.__timestamp: float = timestamp

        self.__balls: list[TrackedBall] = balls

        self.__robots: list[TrackedRobot] = robots

        self.__kicked_ball: KickedBall = kicked_ball

        self.__capabilities: list[Capability] = capabilities

    def __str__(self) -> str:
        return (
            "TrackedFrame("
            f"frame_number={self.frame_number:d}, "
            f"timestamp={self.timestamp:.3f}, "
            f"balls={self.balls!s}, "
            f"robots={self.robots!s}, "
            f"kicked_ball={self.kicked_ball!s}, "
            f"capabilities={self.capabilities!s}"
            ")"
        )

    def __repr__(self) -> str:
        return (
            "TrackedFrame("
            f"{self.frame_number}, "
            f"{self.timestamp}, "
            f"{self.balls}, "
            f"{self.robots}, "
            f"{self.kicked_ball}, "
            f"{self.capabilities}"
            ")"
        )

    @property
    def frame_number(self) -> int:
        """frame_number

        Returns:
            int: frame number
        """
        return self.__frame_number

    @property
    def timestamp(self) -> float:
        """timestamp

        Returns:
            float: timestamp
        """
        return self.__timestamp

    @property
    def balls(self) -> list[TrackedBall]:
        """balls

        Returns:
            list[TrackedBall]: balls
        """
        return self.__balls

    @property
    def robots(self) -> list[TrackedRobot]:
        """robots

        Returns:
            list[TrackedRobot]: robots
        """
        return self.__robots

    @property
    def kicked_ball(self) -> KickedBall:
        """kicked_ball

        Returns:
            KickedBall: kicked ball
        """
        return self.__kicked_ball

    @property
    def capabilities(self) -> list[Capability]:
        """capabilities

        Returns:
            list[Capability]: capabilities
        """
        return self.__capabilities
