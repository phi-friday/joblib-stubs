import types
import typing
from multiprocessing.context import BaseContext

import typing_extensions

from ._memmapping_reducer import _MmapMode
from ._multiprocessing_helpers import mp as mp
from ._parallel_backends import AutoBatchingMixin as AutoBatchingMixin
from ._parallel_backends import FallbackToBackend as FallbackToBackend
from ._parallel_backends import LokyBackend as LokyBackend
from ._parallel_backends import MultiprocessingBackend as MultiprocessingBackend
from ._parallel_backends import ParallelBackendBase as ParallelBackendBase
from ._parallel_backends import SequentialBackend as SequentialBackend
from ._parallel_backends import ThreadingBackend as ThreadingBackend
from ._utils import _Sentinel
from ._utils import eval_expr as eval_expr
from .disk import memstr_to_bytes as memstr_to_bytes
from .externals import loky as loky
from .logger import Logger as Logger
from .logger import short_format_time as short_format_time

IS_PYPY: bool
BACKENDS: dict[str, type[ParallelBackendBase]]
DEFAULT_BACKEND: str
MAYBE_AVAILABLE_BACKENDS: set[str]
DEFAULT_THREAD_BACKEND: str
EXTERNAL_BACKENDS: dict[str, typing.Callable[[], typing.Any]]
default_parallel_config: dict[str, _Sentinel[typing.Any]]
VALID_BACKEND_HINTS: tuple[str | None, ...]
VALID_BACKEND_CONSTRAINTS: tuple[str | None, ...]

def get_active_backend(
    prefer: str = ..., require: str = ..., verbose: int = ...
) -> tuple[ParallelBackendBase, int]: ...

class parallel_config:  # noqa: N801
    old_parallel_config: dict[str, typing.Any]
    parallel_config: dict[str, typing.Any]
    def __init__(
        self,
        backend: ParallelBackendBase | None = ...,
        *,
        n_jobs: int | None = ...,
        verbose: int | None = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: str | None = ...,
        require: typing.Literal["sharedmem"] | None = ...,
        inner_max_num_threads: int | None = None,
        **backend_params: typing.Any,
    ) -> None: ...
    def __enter__(self) -> dict[str, typing.Any]: ...
    def __exit__(
        self,
        type: type[BaseException] | None,  # noqa: A002
        value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def unregister(self) -> None: ...

class parallel_backend(parallel_config):  # noqa: N801
    old_backend_and_jobs: tuple[ParallelBackendBase, int] | None
    new_backend_and_jobs: tuple[ParallelBackendBase, int]
    def __init__(
        self,
        backend: ParallelBackendBase,
        n_jobs: int = -1,
        inner_max_num_threads: int | None = None,
        **backend_params: typing.Any,
    ) -> None: ...
    def __enter__(self) -> tuple[ParallelBackendBase, int]: ...

DEFAULT_MP_CONTEXT: BaseContext | None
method: str | None

type _BatchedCall[**P, T] = tuple[
    typing.Callable[P, T], tuple[typing.Any, ...], dict[str, typing.Any]
]

class BatchedCalls:
    items: list[_BatchedCall[..., typing.Any]]
    def __init__(
        self,
        iterator_slice: typing.Iterable[_BatchedCall[..., typing.Any]],
        backend_and_jobs: ParallelBackendBase | tuple[ParallelBackendBase, int],
        reducer_callback: typing.Callable[[], typing.Any] | None = None,
        pickle_cache: dict[typing.Any, typing.Any] | None = None,
    ) -> None: ...
    def __call__(self) -> list[typing.Any]: ...
    def __reduce__(self) -> tuple[type[BatchedCalls], tuple[typing.Any, ...]]: ...
    def __len__(self) -> int: ...

TASK_DONE: str
TASK_ERROR: str
TASK_PENDING: str

def cpu_count(only_physical_cores: bool = False) -> int: ...
def delayed[**P, T](
    function: typing.Callable[P, T],
) -> typing.Callable[P, _BatchedCall[P, T]]: ...

class BatchCompletionCallBack:
    dispatch_timestamp: float
    batch_size: int
    parallel: ParallelBackendBase
    parallel_call_id: tuple[str, ...]
    job: typing.Any
    status: str
    def __init__(
        self, dispatch_timestamp: float, batch_size: int, parallel: ParallelBackendBase
    ) -> None: ...
    def register_job(self, job: typing.Any) -> None: ...
    def get_result(self, timeout: float) -> typing.Any: ...
    def get_status(self, timeout: float) -> str: ...
    def __call__(self, out: typing.Any) -> None: ...

def register_parallel_backend(
    name: str, factory: type[ParallelBackendBase], make_default: bool = False
) -> None: ...
def effective_n_jobs(n_jobs: int = -1) -> int: ...

type _ReturnAs = typing.Literal["list", "generator", "generator_unordered"]
_R = typing_extensions.TypeVar(
    "_R",
    infer_variance=True,
    default=typing.Literal["list"],
    bound="_ReturnAs",  # noqa: PYI020
)

class Parallel(Logger, typing.Generic[_R]):
    verbose: int
    timeout: float | None
    pre_dispatch: int | str
    return_as: _R
    return_generator: bool
    return_ordered: bool
    n_jobs: int
    batch_size: int | typing.Literal["auto"]
    def __init__(
        self,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: _ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> None: ...
    #
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> Parallel[typing.Literal["list"]]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: typing.Literal["list"] = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> Parallel[typing.Literal["list"]]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: typing.Literal["generator"] = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> Parallel[typing.Literal["generator"]]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: typing.Literal["generator_unordered"] = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> Parallel[typing.Literal["generator_unordered"]]: ...
    @typing.overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: _ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = None,
        pre_dispatch: int | str = "2 * n_jobs",
        batch_size: int | typing.Literal["auto"] = "auto",
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: _MmapMode | None = ...,
        prefer: typing.Literal["processes", "threads"] | None = ...,
        require: typing.Any = ...,
    ) -> Parallel[typing.Any]: ...
    #
    def __enter__(self) -> typing_extensions.Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...
    def dispatch_next(self) -> None: ...
    def dispatch_one_batch(
        self, iterator: typing.Iterable[_BatchedCall[..., typing.Any]]
    ) -> bool: ...
    def print_progress(self) -> None: ...
    @typing.overload
    def __call__[T](
        self: Parallel[typing.Literal["list"]],
        iterable: typing.Iterable[_BatchedCall[..., T]],
    ) -> list[T]: ...
    @typing.overload
    def __call__[T](
        self: Parallel[typing.Literal["generator"]],
        iterable: typing.Iterable[_BatchedCall[..., T]],
    ) -> typing.Generator[T, None, None]: ...
    @typing.overload
    def __call__[T](
        self: Parallel[typing.Literal["generator_unordered"]],
        iterable: typing.Iterable[_BatchedCall[..., T]],
    ) -> typing.Generator[T, None, None]: ...
    @typing.overload
    def __call__[T](
        self, iterable: typing.Iterable[_BatchedCall[..., T]]
    ) -> list[T] | typing.Generator[T, None, None]: ...
