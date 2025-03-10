from protos import recipe_nutrition_pb2 as _recipe_nutrition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecipeRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RecipeResponse(_message.Message):
    __slots__ = ("id", "title", "description", "ingredients", "directions", "tips", "utensils", "nutrition")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    INGREDIENTS_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONS_FIELD_NUMBER: _ClassVar[int]
    TIPS_FIELD_NUMBER: _ClassVar[int]
    UTENSILS_FIELD_NUMBER: _ClassVar[int]
    NUTRITION_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    ingredients: _containers.RepeatedCompositeFieldContainer[RecipeRecipeIngredient]
    directions: _containers.RepeatedScalarFieldContainer[str]
    tips: _containers.RepeatedScalarFieldContainer[str]
    utensils: _containers.RepeatedScalarFieldContainer[str]
    nutrition: _recipe_nutrition_pb2.RecipeNutrition
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., ingredients: _Optional[_Iterable[_Union[RecipeRecipeIngredient, _Mapping]]] = ..., directions: _Optional[_Iterable[str]] = ..., tips: _Optional[_Iterable[str]] = ..., utensils: _Optional[_Iterable[str]] = ..., nutrition: _Optional[_Union[_recipe_nutrition_pb2.RecipeNutrition, _Mapping]] = ...) -> None: ...

class RecipeRecipeIngredient(_message.Message):
    __slots__ = ("name", "quantity", "unit")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: float
    unit: str
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[float] = ..., unit: _Optional[str] = ...) -> None: ...
