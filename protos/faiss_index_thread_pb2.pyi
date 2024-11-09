from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FaissIndexThreadStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNINITIALIZED: _ClassVar[FaissIndexThreadStatus]
    IN_PROGRESS: _ClassVar[FaissIndexThreadStatus]
    FAILED: _ClassVar[FaissIndexThreadStatus]
    COMPLETED: _ClassVar[FaissIndexThreadStatus]
UNINITIALIZED: FaissIndexThreadStatus
IN_PROGRESS: FaissIndexThreadStatus
FAILED: FaissIndexThreadStatus
COMPLETED: FaissIndexThreadStatus

class FaissIndexThreadRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FaissIndexThreadResponse(_message.Message):
    __slots__ = ("status", "args")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ARGS_FIELD_NUMBER: _ClassVar[int]
    status: FaissIndexThreadStatus
    args: FaissIndexThreadArgs
    def __init__(self, status: _Optional[_Union[FaissIndexThreadStatus, str]] = ..., args: _Optional[_Union[FaissIndexThreadArgs, _Mapping]] = ...) -> None: ...

class FaissIndexThreadArgs(_message.Message):
    __slots__ = ("count", "model", "path")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    count: int
    model: str
    path: str
    def __init__(self, count: _Optional[int] = ..., model: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
