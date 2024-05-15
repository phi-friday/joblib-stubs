import typing
from datetime import timedelta

import typing_extensions
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

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")

FIRST_LINE_TEXT: str
_STORE_BACKENDS: dict[str, type[StoreBackendBase]]
_MmepMode: typing_extensions.TypeAlias = typing.Literal["r+", "r", "w+", "c"]
_AnyAwaitable: typing_extensions.TypeAlias = (
    typing.Awaitable[_T] | typing.Coroutine[typing.Any, typing.Any, _T]
)
_AnyAwaitableCallable: typing_extensions.TypeAlias = (
    typing.Callable[_P, typing.Awaitable[_T]]
    | typing.Callable[_P, typing.Coroutine[typing.Any, typing.Any, _T]]
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
    def __call__(
        self,
        func: _AnyAwaitableCallable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @typing.overload
    def __call__(
        self,
        func: typing.Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> MemorizedFunc[_P, _T]: ...

def extract_first_line(func_code: str) -> tuple[str, int]: ...

class JobLibCollisionWarning(UserWarning): ...

def register_store_backend(
    backend_name: str, backend: type[StoreBackendBase]
) -> None: ...

class MemorizedResult(Logger, typing.Generic[_T]):
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
    def get(self) -> _T: ...
    def clear(self) -> None: ...

class NotMemorizedResult(typing.Generic[_T]):
    value: _T
    valid: bool
    def __init__(self, value: _T) -> None: ...
    def get(self) -> _T: ...
    def clear(self) -> None: ...

class NotMemorizedFunc(typing.Generic[_P, _T]):
    func: typing.Callable[_P, _T]
    def __init__(self, func: typing.Callable[_P, _T]) -> None: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...
    def call_and_shelve(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> NotMemorizedResult[_T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[_T, dict[typing.Any, typing.Any]]: ...
    def check_call_in_cache(self, *args: typing.Any, **kwargs: typing.Any) -> bool: ...

class AsyncNotMemorizedFunc(
    NotMemorizedFunc[_P, _AnyAwaitable[_T]], typing.Generic[_P, _T]
):
    func: _AnyAwaitableCallable[_P, _T]
    def __init__(self, func: _AnyAwaitableCallable[_P, _T]) -> None: ...
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _AnyAwaitable[_T]: ...
    async def call_and_shelve(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> NotMemorizedResult[_T]: ...
    def call(self) -> tuple[_AnyAwaitable[_T], dict[typing.Any, typing.Any]]: ...  # type: ignore[override]

class MemorizedFunc(Logger, typing.Generic[_P, _T]):
    mmap_mode: _MmepMode
    compress: bool | int
    func: typing.Callable[_P, _T]
    cache_validation_callback: typing.Callable[..., typing.Any] | None
    func_id: str
    ignore: list[str]
    store_backend: StoreBackendBase
    timestamp: float
    __doc__: str
    def __init__(
        self,
        func: typing.Callable[_P, _T],
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
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    def __call__(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    def check_call_in_cache(self, *args: _P.args, **kwargs: _P.kwargs) -> bool: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[MemorizedResult[_T] | NotMemorizedResult[_T], dict[str, typing.Any]]: ...

class AsyncMemorizedFunc(MemorizedFunc[_P, _AnyAwaitable[_T]], typing.Generic[_P, _T]):
    func: _AnyAwaitableCallable[_P, _T]
    def __init__(
        self,
        func: _AnyAwaitableCallable[_P, _T],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: _MmepMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> None: ...
    async def __call__(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    async def call_and_shelve(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> MemorizedResult[_T] | NotMemorizedResult[_T]: ...
    async def call(  # type: ignore[override]
        self, *args: _P.args, **kwargs: _P.kwargs
    ) -> tuple[MemorizedResult[_T] | NotMemorizedResult[_T], dict[str, typing.Any]]: ...

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
    def cache(
        self,
        func: _AnyAwaitableCallable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @typing.overload
    def cache(
        self,
        func: typing.Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: _MmepMode | bool = ...,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = ...,
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
    @typing.overload
    def eval(
        self, func: _AnyAwaitableCallable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> typing.Coroutine[
        typing.Any, typing.Any, _T | NotMemorizedResult[_T] | MemorizedResult[_T]
    ]: ...
    @typing.overload
    def eval(
        self, func: typing.Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> _T | NotMemorizedResult[_T] | MemorizedResult[_T]: ...

def expires_after(
    days: int = ...,
    seconds: int = ...,
    microseconds: int = ...,
    milliseconds: int = ...,
    minutes: int = ...,
    hours: int = ...,
    weeks: int = ...,
) -> typing.Callable[[dict[str, typing.Any]], bool]: ...
