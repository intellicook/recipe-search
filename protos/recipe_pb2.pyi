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
    __slots__ = ("name", "ingredients", "instructions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., instructions: _Optional[_Iterable[str]] = ...) -> None: ...
