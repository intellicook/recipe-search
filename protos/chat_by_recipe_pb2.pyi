from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatByRecipeRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER: _ClassVar[ChatByRecipeRole]
    ASSISTANT: _ClassVar[ChatByRecipeRole]
USER: ChatByRecipeRole
ASSISTANT: ChatByRecipeRole

class ChatByRecipeRequest(_message.Message):
    __slots__ = ("id", "username", "name", "messages")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    id: int
    username: str
    name: str
    messages: _containers.RepeatedCompositeFieldContainer[ChatByRecipeMessage]
    def __init__(self, id: _Optional[int] = ..., username: _Optional[str] = ..., name: _Optional[str] = ..., messages: _Optional[_Iterable[_Union[ChatByRecipeMessage, _Mapping]]] = ...) -> None: ...

class ChatByRecipeResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: ChatByRecipeMessage
    def __init__(self, message: _Optional[_Union[ChatByRecipeMessage, _Mapping]] = ...) -> None: ...

class ChatByRecipeStreamResponse(_message.Message):
    __slots__ = ("header", "content")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    header: ChatByRecipeStreamHeader
    content: ChatByRecipeStreamContent
    def __init__(self, header: _Optional[_Union[ChatByRecipeStreamHeader, _Mapping]] = ..., content: _Optional[_Union[ChatByRecipeStreamContent, _Mapping]] = ...) -> None: ...

class ChatByRecipeMessage(_message.Message):
    __slots__ = ("role", "text")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    role: ChatByRecipeRole
    text: str
    def __init__(self, role: _Optional[_Union[ChatByRecipeRole, str]] = ..., text: _Optional[str] = ...) -> None: ...

class ChatByRecipeStreamHeader(_message.Message):
    __slots__ = ("role",)
    ROLE_FIELD_NUMBER: _ClassVar[int]
    role: ChatByRecipeRole
    def __init__(self, role: _Optional[_Union[ChatByRecipeRole, str]] = ...) -> None: ...

class ChatByRecipeStreamContent(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
