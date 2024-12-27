from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SearchRecipesMatchField(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NAME: _ClassVar[SearchRecipesMatchField]
    INGREDIENTS: _ClassVar[SearchRecipesMatchField]
NAME: SearchRecipesMatchField
INGREDIENTS: SearchRecipesMatchField

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
    __slots__ = ("id", "name", "ingredients", "matches", "detail")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    ingredients: _containers.RepeatedScalarFieldContainer[str]
    matches: _containers.RepeatedCompositeFieldContainer[SearchRecipesMatch]
    detail: SearchRecipesRecipeDetail
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., ingredients: _Optional[_Iterable[str]] = ..., matches: _Optional[_Iterable[_Union[SearchRecipesMatch, _Mapping]]] = ..., detail: _Optional[_Union[SearchRecipesRecipeDetail, _Mapping]] = ...) -> None: ...

class SearchRecipesMatch(_message.Message):
    __slots__ = ("field", "tokens", "index")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    field: SearchRecipesMatchField
    tokens: _containers.RepeatedScalarFieldContainer[str]
    index: int
    def __init__(self, field: _Optional[_Union[SearchRecipesMatchField, str]] = ..., tokens: _Optional[_Iterable[str]] = ..., index: _Optional[int] = ...) -> None: ...

class SearchRecipesRecipeDetail(_message.Message):
    __slots__ = ("instructions", "raw")
    INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    instructions: _containers.RepeatedScalarFieldContainer[str]
    raw: str
    def __init__(self, instructions: _Optional[_Iterable[str]] = ..., raw: _Optional[str] = ...) -> None: ...
