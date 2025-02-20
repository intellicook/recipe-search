from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecipeNutritionValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECIPE_NUTRITION_VALUE_HIGH: _ClassVar[RecipeNutritionValue]
    RECIPE_NUTRITION_VALUE_MEDIUM: _ClassVar[RecipeNutritionValue]
    RECIPE_NUTRITION_VALUE_LOW: _ClassVar[RecipeNutritionValue]
    RECIPE_NUTRITION_VALUE_NONE: _ClassVar[RecipeNutritionValue]
RECIPE_NUTRITION_VALUE_HIGH: RecipeNutritionValue
RECIPE_NUTRITION_VALUE_MEDIUM: RecipeNutritionValue
RECIPE_NUTRITION_VALUE_LOW: RecipeNutritionValue
RECIPE_NUTRITION_VALUE_NONE: RecipeNutritionValue

class RecipeNutrition(_message.Message):
    __slots__ = ("calories", "fat", "protein", "carbs")
    CALORIES_FIELD_NUMBER: _ClassVar[int]
    FAT_FIELD_NUMBER: _ClassVar[int]
    PROTEIN_FIELD_NUMBER: _ClassVar[int]
    CARBS_FIELD_NUMBER: _ClassVar[int]
    calories: RecipeNutritionValue
    fat: RecipeNutritionValue
    protein: RecipeNutritionValue
    carbs: RecipeNutritionValue
    def __init__(self, calories: _Optional[_Union[RecipeNutritionValue, str]] = ..., fat: _Optional[_Union[RecipeNutritionValue, str]] = ..., protein: _Optional[_Union[RecipeNutritionValue, str]] = ..., carbs: _Optional[_Union[RecipeNutritionValue, str]] = ...) -> None: ...
