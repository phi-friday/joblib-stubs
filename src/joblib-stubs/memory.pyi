import typing
from datetime import timedelta

from joblib import hashing as hashing
from joblib._store_backends import CacheWarning as CacheWarning
from joblib._store_backends import FileSystemStoreBackend as FileSystemStoreBackend
from joblib._store_backends import StoreBackendBase as StoreBackendBase
from joblib.func_inspect import filter_args as filter_args
from joblib.func_inspect import format_call as format_call
from joblib.func_inspect import format_signature as format_signature
from joblib.func_inspect import get_func_code as get_func_code
from joblib.func_inspect import get_func_name as get_func_name
from joblib.logger import Logger as Logger
from joblib.logger import format_time as format_time
from joblib.logger import pformat as pformat

FIRST_LINE_TEXT: str
_STORE_BACKENDS: dict[str, type[StoreBackendBase]]
type _MmepMode = typing.Literal["r+", "r", "w+", "c"]
type _AnyAwaitable[T] = (
    typing.Awaitable[T] | typing.Coroutine[typing.Any, typing.Any, T]
)
type _AnyAwaitableCallable[**P, T] = (
    typing.Callable[P, typing.Awaitable[T]]
    | typing.Callable[P, typing.Coroutine[typing.Any, typing.Any, T]]
)

class _CacheFunc(typing.Protocol):
    @typing.overload
    def __call__(
        self,
        func: None,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> _CacheFunc: ...
    @typing.overload
    def __call__[**P, T](
        self,
        func: _AnyAwaitableCallable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> AsyncMemorizedFunc[P, T]: ...
    @typing.overload
    def __call__[**P, T](
        self,
        func: typing.Callable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> MemorizedFunc[P, T]: ...

def extract_first_line(func_code: str) -> tuple[str, int]: ...

class JobLibCollisionWarning(UserWarning): ...

def register_store_backend(
    backend_name: str, backend: type[StoreBackendBase]
) -> None: ...

class MemorizedResult[T](Logger):
    store_backend: StoreBackendBase
    mmap_mode: _MmepMode
    metadata: dict[str, typing.Any]
    duration: float
    verbose: int
    timestamp: float
    def __init__(
        self,
        location: str,
        call_id: tuple[str, ...],
        backend: str = ...,
        mmap_mode: _MmepMode | None = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        metadata: dict[str, typing.Any] | None = ...,
    ) -> None: ...
    @property
    def func(self) -> str: ...
    @property
    def func_id(self) -> str: ...
    @property
    def args_id(self) -> str: ...
    @property
    def argument_hash(self) -> str: ...
    def get(self) -> T: ...
    def clear(self) -> None: ...

class NotMemorizedResult[T]:
    value: T
    valid: bool
    def __init__(self, value: T) -> None: ...
    def get(self) -> T: ...
    def clear(self) -> None: ...

class NotMemorizedFunc[**P, T]:
    func: typing.Callable[P, T]
    def __init__(self, func: typing.Callable[P, T]) -> None: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> NotMemorizedResult[T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[T, dict[typing.Any, typing.Any]]: ...
    def check_call_in_cache(self, *args: typing.Any, **kwargs: typing.Any) -> bool: ...

class AsyncNotMemorizedFunc[**P, T](NotMemorizedFunc[P, _AnyAwaitable[T]]):
    func: _AnyAwaitableCallable[P, T]
    def __init__(self, func: _AnyAwaitableCallable[P, T]) -> None: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> _AnyAwaitable[T]: ...
    async def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> NotMemorizedResult[T]: ...
    def call(self) -> tuple[_AnyAwaitable[T], dict[typing.Any, typing.Any]]: ...

class MemorizedFunc[**P, T](Logger):
    mmap_mode: _MmepMode
    compress: bool | int
    func: typing.Callable[P, T]
    cache_validation_callback: typing.Callable[..., typing.Any] | None
    func_id: str
    ignore: list[str]
    store_backend: StoreBackendBase
    timestamp: float
    __doc__: str
    def __init__(
        self,
        func: typing.Callable[P, T],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: _MmepMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> None: ...
    @property
    def func_code_info(self) -> tuple[typing.Any, ...]: ...
    def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    def check_call_in_cache(self, *args: P.args, **kwargs: P.kwargs) -> bool: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[MemorizedResult[T] | NotMemorizedResult[T], dict[str, typing.Any]]: ...

class AsyncMemorizedFunc[**P, T](MemorizedFunc[P, _AnyAwaitable[T]]):
    func: _AnyAwaitableCallable[P, T]
    def __init__(
        self,
        func: _AnyAwaitableCallable[P, T],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: _MmepMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> None: ...
    async def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    async def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    async def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[MemorizedResult[T] | NotMemorizedResult[T], dict[str, typing.Any]]: ...

class Memory(Logger):
    mmap_mode: _MmepMode
    timestamp: float
    bytes_limit: int | str
    backend: str
    compress: bool | int
    backend_options: dict[str, typing.Any]
    location: str
    store_backend: StoreBackendBase
    def __init__(
        self,
        location: str | None = ...,
        backend: str = ...,
        mmap_mode: _MmepMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        bytes_limit: int | str | None = ...,
        backend_options: dict[str, typing.Any] | None = ...,
    ) -> None: ...
    @typing.overload
    def cache(
        self,
        func: None,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> _CacheFunc: ...
    @typing.overload
    def cache[**P, T](
        self,
        func: _AnyAwaitableCallable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> AsyncMemorizedFunc[P, T]: ...
    @typing.overload
    def cache[**P, T](
        self,
        func: typing.Callable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> MemorizedFunc[P, T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def reduce_size(
        self,
        bytes_limit: int | str | None = ...,
        items_limit: int | None = ...,
        age_limit: timedelta | None = ...,
    ) -> None: ...
    @typing.overload
    def eval[**P, T](
        self, func: _AnyAwaitableCallable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> typing.Coroutine[
        typing.Any, typing.Any, T | NotMemorizedResult[T] | MemorizedResult[T]
    ]: ...
    @typing.overload
    def eval[**P, T](
        self, func: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> T | NotMemorizedResult[T] | MemorizedResult[T]: ...

def expires_after(
    days: int = ...,
    seconds: int = ...,
    microseconds: int = ...,
    milliseconds: int = ...,
    minutes: int = ...,
    hours: int = ...,
    weeks: int = ...,
) -> typing.Callable[[dict[str, typing.Any]], bool]: ...
