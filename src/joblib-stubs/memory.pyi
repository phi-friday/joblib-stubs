from collections.abc import Awaitable, Callable, Coroutine
from datetime import timedelta
from pathlib import Path
from typing import Any, overload

from joblib import hashing as hashing
from joblib._store_backends import CacheWarning as CacheWarning
from joblib._store_backends import FileSystemStoreBackend as FileSystemStoreBackend
from joblib._store_backends import StoreBackendBase as StoreBackendBase
from joblib._typeshed import MemoryCacheFunc, MmapMode
from joblib.func_inspect import filter_args as filter_args
from joblib.func_inspect import format_call as format_call
from joblib.func_inspect import format_signature as format_signature
from joblib.func_inspect import get_func_code as get_func_code
from joblib.func_inspect import get_func_name as get_func_name
from joblib.logger import Logger as Logger
from joblib.logger import format_time as format_time
from joblib.logger import pformat as pformat

FIRST_LINE_TEXT: str

def extract_first_line(func_code: str) -> tuple[str, int]: ...

class JobLibCollisionWarning(UserWarning): ...

def register_store_backend(
    backend_name: str, backend: type[StoreBackendBase]
) -> None: ...

class MemorizedResult[T](Logger):
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
    def get(self) -> T: ...
    def clear(self) -> None: ...

class NotMemorizedResult[T]:
    value: T
    valid: bool
    def __init__(self, value: T) -> None: ...
    def get(self) -> T: ...
    def clear(self) -> None: ...

class NotMemorizedFunc[**P, T]:
    func: Callable[P, T]
    def __init__(self, func: Callable[P, T]) -> None: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    def call_and_shelve(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> NotMemorizedResult[T]: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(self, *args: P.args, **kwargs: P.kwargs) -> tuple[T, dict[Any, Any]]: ...
    def check_call_in_cache(self, *args: Any, **kwargs: Any) -> bool: ...

class AsyncNotMemorizedFunc[**P, T](NotMemorizedFunc[P, Awaitable[T]]):
    func: Callable[P, Awaitable[T]]
    def __init__(self, func: Callable[P, Awaitable[T]]) -> None: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Awaitable[T]: ...
    async def call_and_shelve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, *args: P.args, **kwargs: P.kwargs
    ) -> NotMemorizedResult[T]: ...
    def call(self) -> tuple[Awaitable[T], dict[Any, Any]]: ...  # pyright: ignore[reportIncompatibleMethodOverride]

class MemorizedFunc[**P, T](Logger):
    mmap_mode: MmapMode
    compress: bool | int
    func: Callable[P, T]
    cache_validation_callback: Callable[..., Any] | None
    func_id: str
    ignore: list[str]
    store_backend: StoreBackendBase
    timestamp: float
    __doc__: str
    def __init__(
        self,
        func: Callable[P, T],
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
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    def check_call_in_cache(self, *args: P.args, **kwargs: P.kwargs) -> bool: ...
    def clear(self, warn: bool = ...) -> None: ...
    def call(self, *args: P.args, **kwargs: P.kwargs) -> tuple[T, dict[str, Any]]: ...

class AsyncMemorizedFunc[**P, T](MemorizedFunc[P, Awaitable[T]]):
    func: Callable[P, Awaitable[T]]
    def __init__(
        self,
        func: Callable[P, Awaitable[T]],
        location: str,
        backend: str = ...,
        ignore: list[str] | None = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        timestamp: float | None = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> None: ...
    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...
    async def call_and_shelve(  # pyright: ignore[reportIncompatibleVariableOverride,reportIncompatibleMethodOverride]
        self, *args: P.args, **kwargs: P.kwargs
    ) -> MemorizedResult[T] | NotMemorizedResult[T]: ...
    async def call(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, *args: P.args, **kwargs: P.kwargs
    ) -> tuple[T, dict[str, Any]]: ...

class Memory(Logger):
    mmap_mode: MmapMode
    timestamp: float
    backend: str
    compress: bool | int
    backend_options: dict[str, Any]
    location: str | Path
    store_backend: StoreBackendBase
    def __init__(
        self,
        location: str | Path | None = ...,
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
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
    ) -> MemoryCacheFunc: ...
    @overload
    def cache[**P, T](
        self,
        func: Callable[P, Awaitable[T]],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[P, T]: ...
    @overload
    def cache[**P, T](
        self,
        func: Callable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[P, T]: ...
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
    def eval[**P, T](
        self, func: Callable[P, Awaitable[T]], *args: P.args, **kwargs: P.kwargs
    ) -> Coroutine[Any, Any, T]: ...
    @overload
    def eval[**P, T](
        self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> T: ...

def expires_after(
    days: int = ...,
    seconds: int = ...,
    microseconds: int = ...,
    milliseconds: int = ...,
    minutes: int = ...,
    hours: int = ...,
    weeks: int = ...,
) -> Callable[[dict[str, Any]], bool]: ...
