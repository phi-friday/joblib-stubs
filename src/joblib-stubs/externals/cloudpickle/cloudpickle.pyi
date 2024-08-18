import pickle
import threading
import weakref
from types import ModuleType
from typing import Any, Callable, ClassVar, Mapping

from _typeshed import ReadableBuffer, SupportsWrite
from joblib._typeshed import Dispatch, EmptyCellValueClass, Reducer
from typing_extensions import Concatenate, TypeAlias, TypeVar

_T = TypeVar("_T")

_PICKLE_BY_VALUE_MODULES: set[str]
_DYNAMIC_CLASS_TRACKER_BY_CLASS: weakref.WeakKeyDictionary[Any, str]
_DYNAMIC_CLASS_TRACKER_BY_ID: weakref.WeakValueDictionary[str, Any]
_DYNAMIC_CLASS_TRACKER_LOCK: threading.Lock

DEFAULT_PROTOCOL: int
PYPY: bool
builtin_code_type: type[Any] | None

def register_pickle_by_value(module: ModuleType) -> None: ...
def unregister_pickle_by_value(module: ModuleType) -> None: ...
def list_registry_pickle_by_value() -> set[str]: ...

STORE_GLOBAL: int
DELETE_GLOBAL: int
LOAD_GLOBAL: int
GLOBAL_OPS: tuple[int, int, int]
HAVE_ARGUMENT: int
EXTENDED_ARG: int

def is_tornado_coroutine(func: Callable[..., Any]) -> bool: ...
def subimport(name: str) -> ModuleType: ...
def dynamic_subimport(
    name: str,
    vars: Mapping[str, Any],  # noqa: A002
) -> ModuleType: ...
def instance(cls: type[_T]) -> _T: ...

_empty_cell_value: EmptyCellValueClass

class _PickleBuffer:
    def __init__(self, buffer: ReadableBuffer) -> None: ...
    def raw(self) -> memoryview: ...
    def release(self) -> None: ...
    def __buffer__(self, flags: int, /) -> memoryview: ...
    def __release_buffer__(self, buffer: memoryview, /) -> None: ...

_BufferCallback: TypeAlias = Callable[[_PickleBuffer], Any] | None

class Pickler(pickle.Pickler):
    dispatch_table: ClassVar[dict[type[Any], Reducer[Any]]]  # type: ignore[misc]
    def dump(self, obj: Any) -> None: ...
    globals_ref: dict[int, dict[str, Any]]
    proto: int
    def __init__(
        self,
        file: SupportsWrite[bytes],
        protocol: int | None = ...,
        buffer_callback: _BufferCallback | None = ...,
    ) -> None: ...
    dispatch: ClassVar[dict[type[Any], Dispatch[Any]]]
    def reducer_override(self, obj: Any) -> Any: ...
    def save_global(
        self,
        obj: Any,
        name: str | None = ...,
        pack: Callable[Concatenate[str | bytes, ...], bytes] = ...,
    ) -> None: ...
    def save_function(self, obj: Any, name: str | None = ...) -> None: ...
    def save_pypy_builtin_func(self, obj: Any) -> None: ...

def dump(
    obj: Any,
    file: SupportsWrite[bytes],
    protocol: int | None = ...,
    buffer_callback: _BufferCallback | None = ...,
) -> None: ...
def dumps(
    obj: Any, protocol: int | None = ..., buffer_callback: _BufferCallback | None = ...
) -> bytes: ...

load = pickle.load
loads = pickle.loads
CloudPickler = Pickler
