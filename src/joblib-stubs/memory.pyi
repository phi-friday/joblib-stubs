from datetime import timedelta
from typing import Any, Callable, Coroutine, Generic, Protocol, overload

from joblib import hashing as hashing
from joblib._store_backends import CacheWarning as CacheWarning
from joblib._store_backends import FileSystemStoreBackend as FileSystemStoreBackend
from joblib._store_backends import StoreBackendBase as StoreBackendBase
from joblib._typeshed import AnyAwaitable, AnyAwaitableCallable, MmapMode
from joblib.func_inspect import filter_args as filter_args
from joblib.func_inspect import format_call as format_call
from joblib.func_inspect import format_signature as format_signature
from joblib.func_inspect import get_func_code as get_func_code
from joblib.func_inspect import get_func_name as get_func_name
from joblib.logger import Logger as Logger
from joblib.logger import format_time as format_time
from joblib.logger import pformat as pformat
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

FIRST_LINE_TEXT: str
_STORE_BACKENDS: dict[str, type[StoreBackendBase]]

class _CacheFunc(Protocol):
    @overload
    def __call__(
        self,
        func: None,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> _CacheFunc: ...
    @overload
    def __call__(
        self,
        func: AnyAwaitableCallable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @overload
    def __call__(
        self,
        func: Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[_P, _T]: ...

def extract_first_line(func_code: str) -> tuple[str, int]: ...

class JobLibCollisionWarning(UserWarning): ...

def register_store_backend(
    backend_name: str, backend: type[StoreBackendBase]
) -> None: ...

class MemorizedResult(Logger, Generic[_T]):
    store_backend: StoreBackendBase
    mmap_mode: MmapMode
    metadata: dict[str, Any]
    duration: float
    verbose: int
    timestamp: float
    def __init__(
        self,
        location: str,
        call_id: tuple[str, ...],
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        metadata: dict[str, Any] | None = ...,
    ) -> None: ...
    @property
    def func(self) -> str: ...
    @property
    def func_id(self) -> str: ...
    @property
    def args_id(self) -> str: ...
    @property
    def argument_hash(self) -> str: ...
    def get(self) -> _T: ...
    def clear(self) -> None: ...

class NotMemorizedResult(Generic[_T]):
    value: _T
    valid: bool
    def __init__(self, value: _T) -> None: ...
    def get(self) -> _T: ...
    def clear(self) -> None: ...

class NotMemorizedFunc(Generic[_P, _T]):
    func: Callable[_P, _T]
    def __init__(self, func: Callable[_P, _T]) -> None: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def call_and_shelve(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> NotMemorizedResult[_T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[_T, dict[Any, Any]]: ...
    def check_call_in_cache(self, *args: Any, **kwargs: Any) -> bool: ...

class AsyncNotMemorizedFunc(NotMemorizedFunc[_P, AnyAwaitable[_T]], Generic[_P, _T]):
    func: AnyAwaitableCallable[_P, _T]  # pyright: ignore[reportIncompatibleMethodOverride]
    def __init__(self, func: AnyAwaitableCallable[_P, _T]) -> None: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> AnyAwaitable[_T]: ...
    async def call_and_shelve(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> NotMemorizedResult[_T]: ...
    def call(self) -> tuple[AnyAwaitable[_T], dict[Any, Any]]: ...  # type: ignore[override]

class MemorizedFunc(Logger, Generic[_P, _T]):
    mmap_mode: MmapMode
    compress: bool | int
    func: Callable[_P, _T]
    cache_validation_callback: Callable[..., Any] | None
    func_id: str
    ignore: list[str]
    store_backend: StoreBackendBase
    timestamp: float
    __doc__: str
    def __init__(
        self,
        func: Callable[_P, _T],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> None: ...
    @property
    def func_code_info(self) -> tuple[Any, ...]: ...
    def call_and_shelve(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def check_call_in_cache(self, *args: _P.args, **kwargs: _P.kwargs) -> bool: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[_T, dict[str, Any]]: ...

class AsyncMemorizedFunc(MemorizedFunc[_P, AnyAwaitable[_T]], Generic[_P, _T]):
    func: AnyAwaitableCallable[_P, _T]  # pyright: ignore[reportIncompatibleMethodOverride]
    def __init__(
        self,
        func: AnyAwaitableCallable[_P, _T],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> None: ...
    async def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    async def call_and_shelve(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    async def call(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[_T, dict[str, Any]]: ...

class Memory(Logger):
    mmap_mode: MmapMode
    timestamp: float
    bytes_limit: int | str
    backend: str
    compress: bool | int
    backend_options: dict[str, Any]
    location: str
    store_backend: StoreBackendBase
    def __init__(
        self,
        location: str | None = ...,
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        bytes_limit: int | str | None = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
    @overload
    def cache(
        self,
        func: None = ...,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> _CacheFunc: ...
    @overload
    def cache(
        self,
        func: AnyAwaitableCallable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @overload
    def cache(
        self,
        func: Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[_P, _T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def reduce_size(
        self,
        bytes_limit: int | str | None = ...,
        items_limit: int | None = ...,
        age_limit: timedelta | None = ...,
    ) -> None: ...
    # awaitble -> awaitable
    # non-awaitable -> non-awaitable
    @overload
    def eval(
        self, func: AnyAwaitableCallable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> Coroutine[Any, Any, _T]: ...
    @overload
    def eval(
        self, func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> _T: ...

def expires_after(
    days: int = ...,
    seconds: int = ...,
    microseconds: int = ...,
    milliseconds: int = ...,
    minutes: int = ...,
    hours: int = ...,
    weeks: int = ...,
) -> Callable[[dict[str, Any]], bool]: ...
