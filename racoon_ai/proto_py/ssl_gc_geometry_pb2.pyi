"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Vector2(google.protobuf.message.Message):
    """A vector with two dimensions"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    x: builtins.float = ...
    y: builtins.float = ...
    def __init__(self,
        *,
        x : typing.Optional[builtins.float] = ...,
        y : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y"]) -> None: ...
global___Vector2 = Vector2

class Vector3(google.protobuf.message.Message):
    """A vector with three dimensions"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    x: builtins.float = ...
    y: builtins.float = ...
    z: builtins.float = ...
    def __init__(self,
        *,
        x : typing.Optional[builtins.float] = ...,
        y : typing.Optional[builtins.float] = ...,
        z : typing.Optional[builtins.float] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y","z",b"z"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector3 = Vector3
