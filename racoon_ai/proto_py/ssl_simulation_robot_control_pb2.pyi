"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class RobotCommand(google.protobuf.message.Message):
    """Full command for a single robot"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ID_FIELD_NUMBER: builtins.int
    MOVE_COMMAND_FIELD_NUMBER: builtins.int
    KICK_SPEED_FIELD_NUMBER: builtins.int
    KICK_ANGLE_FIELD_NUMBER: builtins.int
    DRIBBLER_SPEED_FIELD_NUMBER: builtins.int
    id: builtins.int = ...
    """Id of the robot"""

    @property
    def move_command(self) -> global___RobotMoveCommand:
        """Movement command"""
        pass
    kick_speed: builtins.float = ...
    """Absolute (3 dimensional) kick speed [m/s]"""

    kick_angle: builtins.float = ...
    """Kick angle [degree] (defaults to 0 degrees for a straight kick)"""

    dribbler_speed: builtins.float = ...
    """Dribbler speed in rounds per minute [rpm]"""

    def __init__(self,
        *,
        id : typing.Optional[builtins.int] = ...,
        move_command : typing.Optional[global___RobotMoveCommand] = ...,
        kick_speed : typing.Optional[builtins.float] = ...,
        kick_angle : typing.Optional[builtins.float] = ...,
        dribbler_speed : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dribbler_speed",b"dribbler_speed","id",b"id","kick_angle",b"kick_angle","kick_speed",b"kick_speed","move_command",b"move_command"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dribbler_speed",b"dribbler_speed","id",b"id","kick_angle",b"kick_angle","kick_speed",b"kick_speed","move_command",b"move_command"]) -> None: ...
global___RobotCommand = RobotCommand

class RobotMoveCommand(google.protobuf.message.Message):
    """Wrapper for different kinds of movement commands"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    WHEEL_VELOCITY_FIELD_NUMBER: builtins.int
    LOCAL_VELOCITY_FIELD_NUMBER: builtins.int
    GLOBAL_VELOCITY_FIELD_NUMBER: builtins.int
    @property
    def wheel_velocity(self) -> global___MoveWheelVelocity:
        """Move with wheel velocities"""
        pass
    @property
    def local_velocity(self) -> global___MoveLocalVelocity:
        """Move with local velocity"""
        pass
    @property
    def global_velocity(self) -> global___MoveGlobalVelocity:
        """Move with global velocity"""
        pass
    def __init__(self,
        *,
        wheel_velocity : typing.Optional[global___MoveWheelVelocity] = ...,
        local_velocity : typing.Optional[global___MoveLocalVelocity] = ...,
        global_velocity : typing.Optional[global___MoveGlobalVelocity] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["command",b"command","global_velocity",b"global_velocity","local_velocity",b"local_velocity","wheel_velocity",b"wheel_velocity"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["command",b"command","global_velocity",b"global_velocity","local_velocity",b"local_velocity","wheel_velocity",b"wheel_velocity"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["command",b"command"]) -> typing.Optional[typing_extensions.Literal["wheel_velocity","local_velocity","global_velocity"]]: ...
global___RobotMoveCommand = RobotMoveCommand

class MoveWheelVelocity(google.protobuf.message.Message):
    """Move robot with wheel velocities"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FRONT_RIGHT_FIELD_NUMBER: builtins.int
    BACK_RIGHT_FIELD_NUMBER: builtins.int
    BACK_LEFT_FIELD_NUMBER: builtins.int
    FRONT_LEFT_FIELD_NUMBER: builtins.int
    front_right: builtins.float = ...
    """Velocity [m/s] of front right wheel"""

    back_right: builtins.float = ...
    """Velocity [m/s] of back right wheel"""

    back_left: builtins.float = ...
    """Velocity [m/s] of back left wheel"""

    front_left: builtins.float = ...
    """Velocity [m/s] of front left wheel"""

    def __init__(self,
        *,
        front_right : typing.Optional[builtins.float] = ...,
        back_right : typing.Optional[builtins.float] = ...,
        back_left : typing.Optional[builtins.float] = ...,
        front_left : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["back_left",b"back_left","back_right",b"back_right","front_left",b"front_left","front_right",b"front_right"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["back_left",b"back_left","back_right",b"back_right","front_left",b"front_left","front_right",b"front_right"]) -> None: ...
global___MoveWheelVelocity = MoveWheelVelocity

class MoveLocalVelocity(google.protobuf.message.Message):
    """Move robot with local velocity"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FORWARD_FIELD_NUMBER: builtins.int
    LEFT_FIELD_NUMBER: builtins.int
    ANGULAR_FIELD_NUMBER: builtins.int
    forward: builtins.float = ...
    """Velocity forward [m/s] (towards the dribbler)"""

    left: builtins.float = ...
    """Velocity to the left [m/s]"""

    angular: builtins.float = ...
    """Angular velocity counter-clockwise [rad/s]"""

    def __init__(self,
        *,
        forward : typing.Optional[builtins.float] = ...,
        left : typing.Optional[builtins.float] = ...,
        angular : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["angular",b"angular","forward",b"forward","left",b"left"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["angular",b"angular","forward",b"forward","left",b"left"]) -> None: ...
global___MoveLocalVelocity = MoveLocalVelocity

class MoveGlobalVelocity(google.protobuf.message.Message):
    """Move robot with global velocity"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    ANGULAR_FIELD_NUMBER: builtins.int
    x: builtins.float = ...
    """Velocity on x-axis of the field [m/s]"""

    y: builtins.float = ...
    """Velocity on y-axis of the field [m/s]"""

    angular: builtins.float = ...
    """Angular velocity counter-clockwise [rad/s]"""

    def __init__(self,
        *,
        x : typing.Optional[builtins.float] = ...,
        y : typing.Optional[builtins.float] = ...,
        angular : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["angular",b"angular","x",b"x","y",b"y"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["angular",b"angular","x",b"x","y",b"y"]) -> None: ...
global___MoveGlobalVelocity = MoveGlobalVelocity

class RobotControl(google.protobuf.message.Message):
    """Command from the connected client to the simulator"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ROBOT_COMMANDS_FIELD_NUMBER: builtins.int
    @property
    def robot_commands(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RobotCommand]:
        """Control the robots"""
        pass
    def __init__(self,
        *,
        robot_commands : typing.Optional[typing.Iterable[global___RobotCommand]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["robot_commands",b"robot_commands"]) -> None: ...
global___RobotControl = RobotControl
