from concurrent import futures
from multiprocessing.context import BaseContext
from multiprocessing.pool import AsyncResult as AsyncResult
from types import TracebackType
from typing import Any, Callable, Generator, Generic, Iterable, Literal, overload

from joblib._multiprocessing_helpers import mp as mp
from joblib._parallel_backends import AutoBatchingMixin as AutoBatchingMixin
from joblib._parallel_backends import FallbackToBackend as FallbackToBackend
from joblib._parallel_backends import LokyBackend as LokyBackend
from joblib._parallel_backends import MultiprocessingBackend as MultiprocessingBackend
from joblib._parallel_backends import ParallelBackendBase as ParallelBackendBase
from joblib._parallel_backends import SequentialBackend as SequentialBackend
from joblib._parallel_backends import ThreadingBackend as ThreadingBackend
from joblib._typeshed import (
    BatchedCall,
    MmapMode,
    Prefer,
    Require,
    ReturnAs,
    ReturnGererator,
    ReturnGereratorUnordered,
    ReturnList,
    ReturnUnknown,
)
from joblib._utils import _Sentinel
from joblib._utils import eval_expr as eval_expr
from joblib.disk import memstr_to_bytes as memstr_to_bytes
from joblib.externals import loky as loky
from joblib.logger import Logger as Logger
from joblib.logger import short_format_time as short_format_time
from typing_extensions import ParamSpec, Self, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")
_R = TypeVar("_R", default=Literal["list"], bound=ReturnAs)

IS_PYPY: bool
BACKENDS: dict[str, type[ParallelBackendBase[Any]]]
DEFAULT_BACKEND: str
MAYBE_AVAILABLE_BACKENDS: set[str]
DEFAULT_THREAD_BACKEND: str
EXTERNAL_BACKENDS: dict[str, Callable[[], Any]]
default_parallel_config: dict[str, _Sentinel[Any]]
VALID_BACKEND_HINTS: tuple[str | None, ...]
VALID_BACKEND_CONSTRAINTS: tuple[str | None, ...]

def get_active_backend(
    prefer: Prefer | None = ..., require: Require | None = ..., verbose: int = ...
) -> tuple[ParallelBackendBase[Any], int]: ...

class parallel_config:  # noqa: N801
    old_parallel_config: dict[str, Any]
    parallel_config: dict[str, Any]
    def __init__(
        self,
        backend: str | ParallelBackendBase[Any] | None = ...,
        *,
        n_jobs: int | None = ...,
        verbose: int | None = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        inner_max_num_threads: int | None = ...,
        **backend_params: Any,
    ) -> None: ...
    def __enter__(self) -> dict[str, Any]: ...
    def __exit__(
        self,
        type: type[BaseException] | None,  # noqa: A002
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def unregister(self) -> None: ...

class parallel_backend(parallel_config, Generic[_R]):  # noqa: N801
    old_backend_and_jobs: tuple[ParallelBackendBase[Any], int] | None
    new_backend_and_jobs: tuple[ParallelBackendBase[_R], int]
    def __init__(
        self,
        backend: ParallelBackendBase[_R],
        n_jobs: int = ...,
        inner_max_num_threads: int | None = ...,
        **backend_params: Any,
    ) -> None: ...
    def __enter__(self) -> tuple[ParallelBackendBase[_R], int]: ...  # type: ignore[override]

DEFAULT_MP_CONTEXT: BaseContext | None
method: str | None

class BatchedCalls:
    items: list[BatchedCall[..., Any]]
    def __init__(
        self,
        iterator_slice: Iterable[BatchedCall[..., Any]],
        backend_and_jobs: ParallelBackendBase[Any]
        | tuple[ParallelBackendBase[Any], int],
        reducer_callback: Callable[[], Any] | None = ...,
        pickle_cache: dict[Any, Any] | None = ...,
    ) -> None: ...
    def __call__(self) -> list[Any]: ...
    def __reduce__(
        self,
    ) -> tuple[
        type[BatchedCalls],
        tuple[
            list[BatchedCall[..., Any]],
            tuple[ParallelBackendBase[Any], int | None],
            None,
            dict[Any, Any],
        ],
    ]: ...
    def __len__(self) -> int: ...

TASK_DONE: Literal["Done"]
TASK_ERROR: Literal["Error"]
TASK_PENDING: Literal["Pending"]

def cpu_count(only_physical_cores: bool = ...) -> int: ...
def delayed(function: Callable[_P, _T]) -> Callable[_P, BatchedCall[_P, _T]]: ...

class BatchCompletionCallBack(Generic[_T]):
    dispatch_timestamp: float
    batch_size: int
    parallel: Parallel
    parallel_call_id: tuple[str, ...]
    job: futures.Future[_T] | AsyncResult[_T] | None
    status: str
    def __init__(
        self, dispatch_timestamp: float, batch_size: int, parallel: Parallel
    ) -> None: ...
    def register_job(self, job: futures.Future[_T] | AsyncResult[_T]) -> None: ...
    def get_result(self, timeout: float) -> Any: ...
    def get_status(self, timeout: float) -> str: ...
    def __call__(self, out: futures.Future[_T] | AsyncResult[_T]) -> None: ...

def register_parallel_backend(
    name: str, factory: type[ParallelBackendBase[Any]], make_default: bool = ...
) -> None: ...
def effective_n_jobs(n_jobs: int = ...) -> int: ...

class Parallel(Logger, Generic[_R]):
    _backend: ParallelBackendBase[_R]
    _backend_args: dict[str, Any]
    verbose: int
    timeout: float | None
    pre_dispatch: int | str
    return_as: _R
    return_generator: bool
    return_ordered: bool
    n_jobs: int
    batch_size: int | Literal["auto"]
    def __init__(
        self,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[_R] | None = ...,
        return_as: ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> None: ...
    #
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnList] | None = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnList]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnList] | None = ...,
        return_as: ReturnList = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnList]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnGererator] | None = ...,
        return_as: ReturnGererator = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnGererator]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnGereratorUnordered] | None = ...,
        return_as: ReturnGereratorUnordered = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnGereratorUnordered]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnUnknown] | None = ...,
        return_as: ReturnUnknown = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnUnknown]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[Any] | None = ...,
        return_as: ReturnAs = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[Any]: ...
    #
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...
    def dispatch_next(self) -> None: ...
    def dispatch_one_batch(self, iterator: Iterable[BatchedCall[..., Any]]) -> bool: ...
    def print_progress(self) -> None: ...
    @overload
    def __call__(
        self: Parallel[ReturnList], iterable: Iterable[BatchedCall[..., _T]]
    ) -> list[_T]: ...
    @overload
    def __call__(
        self: Parallel[ReturnGererator], iterable: Iterable[BatchedCall[..., _T]]
    ) -> Generator[_T, None, None]: ...
    @overload
    def __call__(
        self: Parallel[ReturnGereratorUnordered],
        iterable: Iterable[BatchedCall[..., _T]],
    ) -> Generator[_T, None, None]: ...
    @overload
    def __call__(
        self: Parallel[ReturnUnknown], iterable: Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | Generator[_T, None, None]: ...
    @overload
    def __call__(
        self: Parallel[Any], iterable: Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | Generator[_T, None, None]: ...
    @overload
    def __call__(
        self, iterable: Iterable[BatchedCall[..., _T]]
    ) -> list[_T] | Generator[_T, None, None]: ...
