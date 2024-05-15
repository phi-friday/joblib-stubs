import typing
from pickle import Pickler
from pickle import loads as loads

import typing_extensions
from _typeshed import SupportsWrite
from joblib.pool import _Reducer

__all__ = ["dump", "dumps", "loads", "register", "set_loky_pickler"]

_T = typing_extensions.TypeVar("_T")

DEFAULT_ENV: str
ENV_LOKY_PICKLER: str

def register(type_: type[_T], reduce_function: _Reducer[_T]) -> None: ...

class _C:
    def f(self) -> None: ...
    @classmethod
    def h(cls) -> None: ...

def set_loky_pickler(loky_pickler: str | None = ...) -> None: ...
def get_loky_pickler_name() -> str: ...
def get_loky_pickler() -> type[Pickler]: ...
def dump(
    obj: typing.Any,
    file: SupportsWrite[bytes],
    reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
    protocol: int | None = ...,
) -> None: ...
def dumps(
    obj: typing.Any,
    reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
    protocol: int | None = ...,
) -> memoryview: ...
