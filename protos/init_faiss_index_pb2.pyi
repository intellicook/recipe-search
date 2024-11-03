from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InitFaissIndexRequest(_message.Message):
    __slots__ = ("count", "path")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    count: int
    path: str
    def __init__(self, count: _Optional[int] = ..., path: _Optional[str] = ...) -> None: ...

class InitFaissIndexResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
