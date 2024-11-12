from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRecipesRequest(_message.Message):
    __slots__ = ("username", "ingredients", "page", "per_page", "include_detail")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    username: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    page: int
    per_page: int
    include_detail: bool
    def __init__(self, username: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., page: _Optional[int] = ..., per_page: _Optional[int] = ..., include_detail: bool = ...) -> None: ...

class SearchRecipesResponse(_message.Message):
    __slots__ = ("recipes",)
    RECIPES_FIELD_NUMBER: _ClassVar[int]
    recipes: _containers.RepeatedCompositeFieldContainer[SearchRecipesRecipe]
    def __init__(self, recipes: _Optional[_Iterable[_Union[SearchRecipesRecipe, _Mapping]]] = ...) -> None: ...

class SearchRecipesRecipe(_message.Message):
    __slots__ = ("id", "name", "ingredients", "detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    detail: SearchRecipesRecipeDetail
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., detail: _Optional[_Union[SearchRecipesRecipeDetail, _Mapping]] = ...) -> None: ...

class SearchRecipesRecipeDetail(_message.Message):
    __slots__ = ("instructions", "raw")
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    raw: str
    def __init__(self, instructions: _Optional[_Iterable[str]] = ..., raw: _Optional[str] = ...) -> None: ...
