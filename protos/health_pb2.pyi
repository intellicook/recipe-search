from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class HealthStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HEALTHY: _ClassVar[HealthStatus]
    DEGRADED: _ClassVar[HealthStatus]
    UNHEALTHY: _ClassVar[HealthStatus]
HEALTHY: HealthStatus
DEGRADED: HealthStatus
UNHEALTHY: HealthStatus

class HealthRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ("status", "checks")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHECKS_FIELD_NUMBER: _ClassVar[int]
    status: HealthStatus
    checks: _containers.RepeatedCompositeFieldContainer[HealthCheck]
    def __init__(self, status: _Optional[_Union[HealthStatus, str]] = ..., checks: _Optional[_Iterable[_Union[HealthCheck, _Mapping]]] = ...) -> None: ...

class HealthCheck(_message.Message):
    __slots__ = ("name", "status")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    name: str
    status: HealthStatus
    def __init__(self, name: _Optional[str] = ..., status: _Optional[_Union[HealthStatus, str]] = ...) -> None: ...
