from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RecipeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RecipeResponse(_message.Message):
    __slots__ = ("id", "name", "ingredients", "instructions", "raw")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    raw: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., instructions: _Optional[_Iterable[str]] = ..., raw: _Optional[str] = ...) -> None: ...
