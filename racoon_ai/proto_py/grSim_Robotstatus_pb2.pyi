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

class Robots_Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ROBOTS_STATUS_FIELD_NUMBER: builtins.int
    @property
    def robots_status(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Robot_Status]: ...
    def __init__(self,
        *,
        robots_status : typing.Optional[typing.Iterable[global___Robot_Status]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["robots_status",b"robots_status"]) -> None: ...
global___Robots_Status = Robots_Status

class Robot_Status(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ROBOT_ID_FIELD_NUMBER: builtins.int
    INFRARED_FIELD_NUMBER: builtins.int
    FLAT_KICK_FIELD_NUMBER: builtins.int
    CHIP_KICK_FIELD_NUMBER: builtins.int
    robot_id: builtins.int = ...
    infrared: builtins.bool = ...
    flat_kick: builtins.bool = ...
    chip_kick: builtins.bool = ...
    def __init__(self,
        *,
        robot_id : typing.Optional[builtins.int] = ...,
        infrared : typing.Optional[builtins.bool] = ...,
        flat_kick : typing.Optional[builtins.bool] = ...,
        chip_kick : typing.Optional[builtins.bool] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["chip_kick",b"chip_kick","flat_kick",b"flat_kick","infrared",b"infrared","robot_id",b"robot_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["chip_kick",b"chip_kick","flat_kick",b"flat_kick","infrared",b"infrared","robot_id",b"robot_id"]) -> None: ...
global___Robot_Status = Robot_Status
