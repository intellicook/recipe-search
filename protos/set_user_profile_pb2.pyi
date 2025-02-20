from protos import user_profile_veggie_identity_pb2 as _user_profile_veggie_identity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetUserProfileRequest(_message.Message):
    __slots__ = ("username", "veggie_identity", "prefer", "dislike")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    VEGGIE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PREFER_FIELD_NUMBER: _ClassVar[int]
    DISLIKE_FIELD_NUMBER: _ClassVar[int]
    username: str
    veggie_identity: _user_profile_veggie_identity_pb2.UserProfileVeggieIdentity
    prefer: _containers.RepeatedScalarFieldContainer[str]
    dislike: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, username: _Optional[str] = ..., veggie_identity: _Optional[_Union[_user_profile_veggie_identity_pb2.UserProfileVeggieIdentity, str]] = ..., prefer: _Optional[_Iterable[str]] = ..., dislike: _Optional[_Iterable[str]] = ...) -> None: ...

class SetUserProfileResponse(_message.Message):
    __slots__ = ("username", "veggie_identity", "prefer", "dislike")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    VEGGIE_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PREFER_FIELD_NUMBER: _ClassVar[int]
    DISLIKE_FIELD_NUMBER: _ClassVar[int]
    username: str
    veggie_identity: _user_profile_veggie_identity_pb2.UserProfileVeggieIdentity
    prefer: _containers.RepeatedScalarFieldContainer[str]
    dislike: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, username: _Optional[str] = ..., veggie_identity: _Optional[_Union[_user_profile_veggie_identity_pb2.UserProfileVeggieIdentity, str]] = ..., prefer: _Optional[_Iterable[str]] = ..., dislike: _Optional[_Iterable[str]] = ...) -> None: ...
