from pickle import Pickler
from pickle import loads as loads
from typing import Any

from _typeshed import SupportsWrite
from joblib._typeshed import Reducer
from typing_extensions import TypeVar

__all__ = ["dump", "dumps", "loads", "register", "set_loky_pickler"]

_T = TypeVar("_T")

DEFAULT_ENV: str
ENV_LOKY_PICKLER: str

def register(type_: type[_T], reduce_function: Reducer[_T]) -> None: ...

class _C:
    def f(self) -> None: ...
    @classmethod
    def h(cls) -> None: ...

def set_loky_pickler(loky_pickler: str | None = ...) -> None: ...
def get_loky_pickler_name() -> str: ...
def get_loky_pickler() -> type[Pickler]: ...
def dump(
    obj: Any,
    file: SupportsWrite[bytes],
    reducers: dict[type[Any], Reducer[Any]] | None = ...,
    protocol: int | None = ...,
) -> None: ...
def dumps(
    obj: Any,
    reducers: dict[type[Any], Reducer[Any]] | None = ...,
    protocol: int | None = ...,
) -> memoryview: ...
