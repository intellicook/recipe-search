# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/add_recipes.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'protos/add_recipes.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from protos import recipe_nutrition_pb2 as protos_dot_recipe__nutrition__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18protos/add_recipes.proto\x1a\x1dprotos/recipe_nutrition.proto\">\n\x11\x41\x64\x64RecipesRequest\x12)\n\x07recipes\x18\x01 \x03(\x0b\x32\x18.AddRecipesRequestRecipe\"@\n\x12\x41\x64\x64RecipesResponse\x12*\n\x07recipes\x18\x01 \x03(\x0b\x32\x19.AddRecipesResponseRecipe\"j\n\x1a\x41\x64\x64RecipesRecipeIngredient\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\x08quantity\x18\x02 \x01(\x02H\x00\x88\x01\x01\x12\x11\n\x04unit\x18\x03 \x01(\tH\x01\x88\x01\x01\x42\x0b\n\t_quantityB\x07\n\x05_unit\"\xc8\x01\n\x17\x41\x64\x64RecipesRequestRecipe\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x30\n\x0bingredients\x18\x03 \x03(\x0b\x32\x1b.AddRecipesRecipeIngredient\x12\x12\n\ndirections\x18\x04 \x03(\t\x12\x0c\n\x04tips\x18\x05 \x03(\t\x12\x10\n\x08utensils\x18\x06 \x03(\t\x12#\n\tnutrition\x18\x07 \x01(\x0b\x32\x10.RecipeNutrition\"\xd5\x01\n\x18\x41\x64\x64RecipesResponseRecipe\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x30\n\x0bingredients\x18\x04 \x03(\x0b\x32\x1b.AddRecipesRecipeIngredient\x12\x12\n\ndirections\x18\x05 \x03(\t\x12\x0c\n\x04tips\x18\x06 \x03(\t\x12\x10\n\x08utensils\x18\x07 \x03(\t\x12#\n\tnutrition\x18\x08 \x01(\x0b\x32\x10.RecipeNutritionB\"\xaa\x02\x1fIntelliCook.RecipeSearch.Clientb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.add_recipes_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\037IntelliCook.RecipeSearch.Client'
  _globals['_ADDRECIPESREQUEST']._serialized_start=59
  _globals['_ADDRECIPESREQUEST']._serialized_end=121
  _globals['_ADDRECIPESRESPONSE']._serialized_start=123
  _globals['_ADDRECIPESRESPONSE']._serialized_end=187
  _globals['_ADDRECIPESRECIPEINGREDIENT']._serialized_start=189
  _globals['_ADDRECIPESRECIPEINGREDIENT']._serialized_end=295
  _globals['_ADDRECIPESREQUESTRECIPE']._serialized_start=298
  _globals['_ADDRECIPESREQUESTRECIPE']._serialized_end=498
  _globals['_ADDRECIPESRESPONSERECIPE']._serialized_start=501
  _globals['_ADDRECIPESRESPONSERECIPE']._serialized_end=714
# @@protoc_insertion_point(module_scope)
