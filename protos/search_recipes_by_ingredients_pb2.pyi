from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRecipesByIngredientsRequest(_message.Message):
    __slots__ = ("username", "ingredients", "limit", "include_detail")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    username: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    limit: int
    include_detail: bool
    def __init__(self, username: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., limit: _Optional[int] = ..., include_detail: bool = ...) -> None: ...

class SearchRecipesByIngredientsResponse(_message.Message):
    __slots__ = ("recipes",)
    RECIPES_FIELD_NUMBER: _ClassVar[int]
    recipes: _containers.RepeatedCompositeFieldContainer[SearchRecipesByIngredientsRecipe]
    def __init__(self, recipes: _Optional[_Iterable[_Union[SearchRecipesByIngredientsRecipe, _Mapping]]] = ...) -> None: ...

class SearchRecipesByIngredientsRecipe(_message.Message):
    __slots__ = ("id", "name", "detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    detail: SearchRecipesByIngredientsRecipeDetail
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., detail: _Optional[_Union[SearchRecipesByIngredientsRecipeDetail, _Mapping]] = ...) -> None: ...

class SearchRecipesByIngredientsRecipeDetail(_message.Message):
    __slots__ = ("ingredients", "instructions", "raw")
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    raw: str
    def __init__(self, ingredients: _Optional[_Iterable[str]] = ..., instructions: _Optional[_Iterable[str]] = ..., raw: _Optional[str] = ...) -> None: ...
