# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: protos/chat_by_recipe.proto
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
    'protos/chat_by_recipe.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bprotos/chat_by_recipe.proto\"i\n\x13\x43hatByRecipeRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12&\n\x08messages\x18\x04 \x03(\x0b\x32\x14.ChatByRecipeMessage\"=\n\x14\x43hatByRecipeResponse\x12%\n\x07message\x18\x01 \x01(\x0b\x32\x14.ChatByRecipeMessage\"\x84\x01\n\x1a\x43hatByRecipeStreamResponse\x12+\n\x06header\x18\x01 \x01(\x0b\x32\x19.ChatByRecipeStreamHeaderH\x00\x12-\n\x07\x63ontent\x18\x02 \x01(\x0b\x32\x1a.ChatByRecipeStreamContentH\x00\x42\n\n\x08response\"D\n\x13\x43hatByRecipeMessage\x12\x1f\n\x04role\x18\x01 \x01(\x0e\x32\x11.ChatByRecipeRole\x12\x0c\n\x04text\x18\x02 \x01(\t\";\n\x18\x43hatByRecipeStreamHeader\x12\x1f\n\x04role\x18\x01 \x01(\x0e\x32\x11.ChatByRecipeRole\")\n\x19\x43hatByRecipeStreamContent\x12\x0c\n\x04text\x18\x01 \x01(\t*+\n\x10\x43hatByRecipeRole\x12\x08\n\x04USER\x10\x00\x12\r\n\tASSISTANT\x10\x01\x42\"\xaa\x02\x1fIntelliCook.RecipeSearch.Clientb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.chat_by_recipe_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\037IntelliCook.RecipeSearch.Client'
  _globals['_CHATBYRECIPEROLE']._serialized_start=510
  _globals['_CHATBYRECIPEROLE']._serialized_end=553
  _globals['_CHATBYRECIPEREQUEST']._serialized_start=31
  _globals['_CHATBYRECIPEREQUEST']._serialized_end=136
  _globals['_CHATBYRECIPERESPONSE']._serialized_start=138
  _globals['_CHATBYRECIPERESPONSE']._serialized_end=199
  _globals['_CHATBYRECIPESTREAMRESPONSE']._serialized_start=202
  _globals['_CHATBYRECIPESTREAMRESPONSE']._serialized_end=334
  _globals['_CHATBYRECIPEMESSAGE']._serialized_start=336
  _globals['_CHATBYRECIPEMESSAGE']._serialized_end=404
  _globals['_CHATBYRECIPESTREAMHEADER']._serialized_start=406
  _globals['_CHATBYRECIPESTREAMHEADER']._serialized_end=465
  _globals['_CHATBYRECIPESTREAMCONTENT']._serialized_start=467
  _globals['_CHATBYRECIPESTREAMCONTENT']._serialized_end=508
# @@protoc_insertion_point(module_scope)
