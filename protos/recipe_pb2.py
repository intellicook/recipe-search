# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/recipe.proto
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
    'protos/recipe.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13protos/recipe.proto\"\x1b\n\rRecipeRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"b\n\x0eRecipeResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0bingredients\x18\x03 \x03(\t\x12\x14\n\x0cinstructions\x18\x04 \x03(\t\x12\x0b\n\x03raw\x18\x05 \x01(\tB\"\xaa\x02\x1fIntelliCook.RecipeSearch.Clientb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.recipe_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\037IntelliCook.RecipeSearch.Client'
  _globals['_RECIPEREQUEST']._serialized_start=23
  _globals['_RECIPEREQUEST']._serialized_end=50
  _globals['_RECIPERESPONSE']._serialized_start=52
  _globals['_RECIPERESPONSE']._serialized_end=150
# @@protoc_insertion_point(module_scope)