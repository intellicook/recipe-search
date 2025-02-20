from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class UserProfileVeggieIdentity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    USER_PROFILE_VEGGIE_IDENTITY_NONE: _ClassVar[UserProfileVeggieIdentity]
    USER_PROFILE_VEGGIE_IDENTITY_VEGETARIAN: _ClassVar[UserProfileVeggieIdentity]
    USER_PROFILE_VEGGIE_IDENTITY_VEGAN: _ClassVar[UserProfileVeggieIdentity]
USER_PROFILE_VEGGIE_IDENTITY_NONE: UserProfileVeggieIdentity
USER_PROFILE_VEGGIE_IDENTITY_VEGETARIAN: UserProfileVeggieIdentity
USER_PROFILE_VEGGIE_IDENTITY_VEGAN: UserProfileVeggieIdentity
