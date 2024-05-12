import pickle
import threading
import types
import typing
import weakref

import typing_extensions
from _typeshed import ReadableBuffer, SupportsWrite
from joblib.pool import _Dispatch as _Dispatch
from joblib.pool import _Reducer as _Reducer

_PICKLE_BY_VALUE_MODULES: set[str]
_DYNAMIC_CLASS_TRACKER_BY_CLASS: weakref.WeakKeyDictionary[typing.Any, str]
_DYNAMIC_CLASS_TRACKER_BY_ID: weakref.WeakValueDictionary[str, typing.Any]
_DYNAMIC_CLASS_TRACKER_LOCK: threading.Lock

DEFAULT_PROTOCOL: int
PYPY: bool
builtin_code_type: type[typing.Any] | None

def register_pickle_by_value(module: types.ModuleType) -> None: ...
def unregister_pickle_by_value(module: types.ModuleType) -> None: ...
def list_registry_pickle_by_value() -> set[str]: ...

STORE_GLOBAL: int
DELETE_GLOBAL: int
LOAD_GLOBAL: int
GLOBAL_OPS: tuple[int, int, int]
HAVE_ARGUMENT: int
EXTENDED_ARG: int

def is_tornado_coroutine(func: typing.Callable[..., typing.Any]) -> bool: ...
def subimport(name: str) -> types.ModuleType: ...
def dynamic_subimport(
    name: str,
    vars: typing.Mapping[str, typing.Any],  # noqa: A002
) -> types.ModuleType: ...
def instance[T](cls: type[T]) -> T: ...

# decorated by `instance`
class _EmptyCellValueClass:
    @classmethod
    def __reduce__(cls) -> str: ...

_empty_cell_value: _EmptyCellValueClass

class _PickleBuffer:
    def __init__(self, buffer: ReadableBuffer) -> None: ...
    def raw(self) -> memoryview: ...
    def release(self) -> None: ...
    def __buffer__(self, flags: int, /) -> memoryview: ...
    def __release_buffer__(self, buffer: memoryview, /) -> None: ...

type _BufferCallback = typing.Callable[[_PickleBuffer], typing.Any] | None

class Pickler(pickle.Pickler):
    dispatch_table: typing.ClassVar[dict[type[typing.Any], _Reducer[typing.Any]]]
    def dump(self, obj: typing.Any) -> None: ...
    globals_ref: dict[int, dict[str, typing.Any]]
    proto: int
    def __init__(
        self,
        file: SupportsWrite[bytes],
        protocol: int | None = ...,
        buffer_callback: _BufferCallback | None = ...,
    ) -> None: ...
    dispatch: typing.ClassVar[dict[type[typing.Any], _Dispatch[typing.Any]]]
    def reducer_override(self, obj: typing.Any) -> typing.Any: ...
    def save_global(
        self,
        obj: typing.Any,
        name: str | None = ...,
        pack: typing.Callable[
            typing_extensions.Concatenate[str | bytes, ...], bytes
        ] = ...,
    ) -> None: ...
    def save_function(self, obj: typing.Any, name: str | None = ...) -> None: ...
    def save_pypy_builtin_func(self, obj: typing.Any) -> None: ...

def dump(
    obj: typing.Any,
    file: SupportsWrite[bytes],
    protocol: int | None = ...,
    buffer_callback: _BufferCallback | None = ...,
) -> None: ...
def dumps(
    obj: typing.Any,
    protocol: int | None = ...,
    buffer_callback: _BufferCallback | None = ...,
) -> bytes: ...

load = pickle.load
loads = pickle.loads
CloudPickler = Pickler
