from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRecipesByIngredientsRequest(_message.Message):
    __slots__ = ("username", "ingredients", "limit")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    username: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    limit: int
    def __init__(self, username: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., limit: _Optional[int] = ...) -> None: ...

class SearchRecipesByIngredientsResponse(_message.Message):
    __slots__ = ("recipes",)
    RECIPES_FIELD_NUMBER: _ClassVar[int]
    recipes: _containers.RepeatedCompositeFieldContainer[SearchRecipesByIngredientsRecipe]
    def __init__(self, recipes: _Optional[_Iterable[_Union[SearchRecipesByIngredientsRecipe, _Mapping]]] = ...) -> None: ...

class SearchRecipesByIngredientsRecipe(_message.Message):
    __slots__ = ("id", "distance", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    distance: float
    name: str
    def __init__(self, id: _Optional[int] = ..., distance: _Optional[float] = ..., name: _Optional[str] = ...) -> None: ...
