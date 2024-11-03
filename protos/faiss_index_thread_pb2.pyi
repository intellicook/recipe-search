from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FaissIndexThreadRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FaissIndexThreadResponse(_message.Message):
    __slots__ = ("args", "is_in_progress", "is_complete", "is_successful")
    ARGS_FIELD_NUMBER: _ClassVar[int]
    IS_IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    IS_COMPLETE_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    args: FaissIndexThreadArgs
    is_in_progress: bool
    is_complete: bool
    is_successful: bool
    def __init__(self, args: _Optional[_Union[FaissIndexThreadArgs, _Mapping]] = ..., is_in_progress: bool = ..., is_complete: bool = ..., is_successful: bool = ...) -> None: ...

class FaissIndexThreadArgs(_message.Message):
    __slots__ = ("count", "model", "path")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    count: int
    model: str
    path: str
    def __init__(self, count: _Optional[int] = ..., model: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...
