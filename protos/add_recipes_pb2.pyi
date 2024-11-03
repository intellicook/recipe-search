from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddRecipesRequest(_message.Message):
    __slots__ = ("recipes",)
    RECIPES_FIELD_NUMBER: _ClassVar[int]
    recipes: _containers.RepeatedCompositeFieldContainer[AddRecipesRecipe]
    def __init__(self, recipes: _Optional[_Iterable[_Union[AddRecipesRecipe, _Mapping]]] = ...) -> None: ...

class AddRecipesResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AddRecipesRecipe(_message.Message):
    __slots__ = ("name", "ingredients", "instructions", "raw")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    name: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    raw: str
    def __init__(self, name: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., instructions: _Optional[_Iterable[str]] = ..., raw: _Optional[str] = ...) -> None: ...
