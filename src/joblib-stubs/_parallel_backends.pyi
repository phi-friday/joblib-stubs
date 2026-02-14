# pyright: reportUnnecessaryTypeIgnoreComment=false
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from concurrent import futures
from contextlib import AbstractContextManager
from multiprocessing.pool import AsyncResult as AsyncResult
from typing import Any, ClassVar, Generic, Literal, NoReturn

from joblib._multiprocessing_helpers import mp as mp
from joblib._typeshed import Prefer, Require, ReturnAs
from joblib.executor import get_memmapping_executor as get_memmapping_executor
from joblib.parallel import Parallel as Parallel
from joblib.pool import MemmappingPool as MemmappingPool
from typing_extensions import TypeVar, deprecated

_R = TypeVar("_R", default=Literal["list"], bound=ReturnAs)
type _AnyContainer[T] = futures.Future[T] | AsyncResult[T]

class ParallelBackendBase(Generic[_R], metaclass=ABCMeta):  # noqa: UP046 (default: +3.13)
    default_n_jobs: ClassVar[int]
    supports_inner_max_num_threads: ClassVar[bool]
    supports_retrieve_callback: ClassVar[bool]
    @property
    def supports_return_generator(self) -> bool: ...
    @property
    def supports_timeout(self) -> bool: ...
    nesting_level: int | None
    inner_max_num_threads: int
    backend_kwargs: dict[str, Any]
    def __init__(
        self,
        nesting_level: int | None = ...,
        inner_max_num_threads: int | None = ...,
        **backend_kwargs: Any,
    ) -> None: ...
    MAX_NUM_THREADS_VARS: ClassVar[list[str]]
    TBB_ENABLE_IPC_VAR: ClassVar[str]
    @abstractmethod
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    @deprecated("implement `submit` instead.")
    def apply_async[T](
        self,
        func: Callable[[], T],
        callback: Callable[[_AnyContainer[T]], Any] | None = ...,
    ) -> _AnyContainer[T]: ...
    def submit[T](
        self,
        func: Callable[[], T],
        callback: Callable[[_AnyContainer[T]], Any] | None = ...,
    ) -> _AnyContainer[T]: ...
    def retrieve_result_callback[T](
        self, out: futures.Future[T] | AsyncResult[T]
    ) -> T: ...
    parallel: Parallel[_R]
    def retrieve_result[T](
        self, out: futures.Future[T] | AsyncResult[T], timeout: float | None = ...
    ) -> T: ...
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        **backend_kwargs: Any,
    ) -> int: ...
    def start_call(self) -> None: ...
    def stop_call(self) -> None: ...
    def terminate(self) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def get_nested_backend(
        self,
    ) -> tuple[SequentialBackend[Any] | ThreadingBackend[Any], int | None]: ...
    def retrieval_context(self) -> AbstractContextManager[None]: ...
    @staticmethod
    def in_main_thread() -> bool: ...

class SequentialBackend(ParallelBackendBase[_R], Generic[_R]):
    uses_threads: ClassVar[bool]
    supports_timeout: ClassVar[bool]  # pyright: ignore[reportIncompatibleMethodOverride]
    supports_retrieve_callback: ClassVar[bool]
    supports_sharedmem: ClassVar[bool]
    def submit(
        self, func: Callable[[], Any], callback: Callable[..., Any] | None = ...
    ) -> NoReturn: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class PoolManagerMixin:
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    def terminate(self) -> None: ...
    def submit[T](
        self,
        func: Callable[[], T],
        callback: Callable[[AsyncResult[T]], Any] | None = ...,
    ) -> AsyncResult[T]: ...
    def retrieve_result_callback(self, out: Any) -> Any: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...

class AutoBatchingMixin(Generic[_R]):
    MIN_IDEAL_BATCH_DURATION: ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: ClassVar[float]
    parallel: Parallel[_R]
    def __init__(self, **kwargs: Any) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def reset_batch_stats(self) -> None: ...

class ThreadingBackend(PoolManagerMixin, ParallelBackendBase[_R], Generic[_R]):
    supports_retrieve_callback: ClassVar[bool]
    uses_threads: ClassVar[bool]
    supports_sharedmem: ClassVar[bool]
    def configure(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        **backend_kwargs: Any,
    ) -> int: ...

class MultiprocessingBackend(
    PoolManagerMixin, AutoBatchingMixin[_R], ParallelBackendBase[_R], Generic[_R]
):
    supports_retrieve_callback: ClassVar[bool]
    supports_return_generator: ClassVar[bool]  # pyright: ignore[reportIncompatibleMethodOverride]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        **memmapping_pool_kwargs: Any,
    ) -> int: ...

class LokyBackend(AutoBatchingMixin[_R], ParallelBackendBase[_R], Generic[_R]):
    supports_retrieve_callback: ClassVar[bool]
    supports_inner_max_num_threads: ClassVar[bool]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        idle_worker_timeout: float = ...,
        **memmapping_executor_kwargs: Any,
    ) -> int: ...
    def terminate(self) -> None: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def submit[T](
        self,
        func: Callable[[], T],
        callback: Callable[[futures.Future[T]], Any] | None = ...,
    ) -> futures.Future[T]: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class FallbackToBackend(Exception):  # noqa: N818
    backend: ParallelBackendBase[Any]
    def __init__(self, backend: ParallelBackendBase[Any]) -> None: ...

def inside_dask_worker() -> bool: ...
