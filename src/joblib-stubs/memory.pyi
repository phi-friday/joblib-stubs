import typing
from datetime import timedelta

from . import hashing as hashing
from ._store_backends import CacheItemInfo
from ._store_backends import CacheWarning as CacheWarning
from ._store_backends import FileSystemStoreBackend as FileSystemStoreBackend
from ._store_backends import StoreBackendBase as StoreBackendBase
from .func_inspect import filter_args as filter_args
from .func_inspect import format_call as format_call
from .func_inspect import format_signature as format_signature
from .func_inspect import get_func_code as get_func_code
from .func_inspect import get_func_name as get_func_name
from .logger import Logger as Logger
from .logger import format_time as format_time
from .logger import pformat as pformat

FIRST_LINE_TEXT: str
_STORE_BACKENDS: dict[str, type[StoreBackendBase]]
type _MmepMode = typing.Literal["r+", "r", "w+", "c"]

class _CacheFunc(typing.Protocol):
    @typing.overload
    def __call__(
        self,
        func: None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> _CacheFunc: ...
    @typing.overload
    def __call__[**P, T](
        self,
        func: typing.Callable[P, T],
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T]: ...
    @typing.overload
    def __call__[**P, T](
        self,
        func: typing.Callable[P, T] | None = None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T] | _CacheFunc: ...
    def __call__[**P, T](
        self,
        func: typing.Callable[P, T] | None = None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T] | _CacheFunc: ...

def extract_first_line(func_code: str) -> tuple[str, int]: ...

class JobLibCollisionWarning(UserWarning): ...

def register_store_backend(
    backend_name: str, backend: type[StoreBackendBase]
) -> None: ...

class MemorizedResult(Logger):
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
        backend: str = "local",
        mmap_mode: _MmepMode | None = None,
        verbose: int = 0,
        timestamp: float | None = None,
        metadata: dict[str, typing.Any] | None = None,
    ) -> None: ...
    @property
    def func(self) -> str: ...
    @property
    def func_id(self) -> str: ...
    @property
    def args_id(self) -> str: ...
    @property
    def argument_hash(self) -> str: ...
    def get(self) -> CacheItemInfo: ...
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
    def clear(self, warn: bool = True) -> None: ...
    def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[T, dict[typing.Any, typing.Any]]: ...
    def check_call_in_cache(self, *args: typing.Any, **kwargs: typing.Any) -> bool: ...

class AsyncNotMemorizedFunc[**P, T: typing.Awaitable](NotMemorizedFunc[P, T]):
    async def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> NotMemorizedResult[typing.Any]: ...  # FIXME: awaitable result

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
        backend: str = "local",
        ignore: list[str] | None = None,
        mmap_mode: _MmepMode | None = None,
        compress: bool | int = False,
        verbose: int = 1,
        timestamp: float | None = None,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> None: ...
    @property
    def func_code_info(self) -> tuple[typing.Any, ...]: ...
    def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult | NotMemorizedResult[T]: ...
    def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult | NotMemorizedResult[T]: ...
    def check_call_in_cache(self, *args: P.args, **kwargs: P.kwargs) -> bool: ...
    def clear(self, warn: bool = True) -> None: ...
    def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[MemorizedResult | NotMemorizedResult[T], dict[str, typing.Any]]: ...

class AsyncMemorizedFunc[**P, T: typing.Awaitable](MemorizedFunc[P, T]):
    async def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> (
        MemorizedResult | NotMemorizedResult[typing.Any]  # FIXME: awaitable result
    ): ...
    async def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> (
        MemorizedResult | NotMemorizedResult[typing.Any]  # FIXME: awaitable result
    ): ...
    async def call(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[
        MemorizedResult | NotMemorizedResult[typing.Any],  # FIXME: awaitable result
        dict[str, typing.Any],
    ]: ...

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
        location: str | None = None,
        backend: str = "local",
        mmap_mode: _MmepMode | None = None,
        compress: bool | int = False,
        verbose: int = 1,
        bytes_limit: int | str | None = None,
        backend_options: dict[str, typing.Any] | None = None,
    ) -> None: ...
    @typing.overload
    def cache(
        self,
        func: None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> _CacheFunc: ...
    @typing.overload
    def cache[**P, T](
        self,
        func: typing.Callable[P, T],
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T]: ...
    @typing.overload
    def cache[**P, T](
        self,
        func: typing.Callable[P, T] | None = None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T] | _CacheFunc: ...
    def cache[**P, T](
        self,
        func: typing.Callable[P, T] | None = None,
        ignore: list[str] | None = None,
        verbose: int | None = None,
        mmap_mode: _MmepMode | bool = False,
        cache_validation_callback: typing.Callable[..., typing.Any] | None = None,
    ) -> MemorizedFunc[P, T] | _CacheFunc: ...
    def clear(self, warn: bool = True) -> None: ...
    def reduce_size(
        self,
        bytes_limit: int | str | None = None,
        items_limit: int | None = None,
        age_limit: timedelta | None = None,
    ) -> None: ...
    def eval[**P, T](
        self, func: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> T | NotMemorizedResult[T] | MemorizedResult: ...

def expires_after(
    days: int = 0,
    seconds: int = 0,
    microseconds: int = 0,
    milliseconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    weeks: int = 0,
) -> typing.Callable[[dict[str, typing.Any]], bool]: ...
