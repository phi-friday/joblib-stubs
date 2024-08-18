# pyright: reportUnnecessaryTypeIgnoreComment=false
from abc import ABCMeta, abstractmethod
from collections.abc import Generator
from concurrent import futures
from multiprocessing.pool import AsyncResult as AsyncResult
from typing import Any, Callable, ClassVar, Generic, Literal, NoReturn

from joblib._multiprocessing_helpers import mp as mp
from joblib._typeshed import AnyContainer, Prefer, Require, ReturnAs
from joblib.executor import get_memmapping_executor as get_memmapping_executor
from joblib.externals.loky import cpu_count as cpu_count
from joblib.externals.loky import process_executor as process_executor
from joblib.externals.loky.process_executor import (
    ShutdownExecutorError as ShutdownExecutorError,
)
from joblib.parallel import Parallel as Parallel
from joblib.pool import MemmappingPool as MemmappingPool
from typing_extensions import TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R", default=Literal["list"], bound=ReturnAs)

class ParallelBackendBase(Generic[_R], metaclass=ABCMeta):
    supports_inner_max_num_threads: ClassVar[bool]
    supports_retrieve_callback: ClassVar[bool]
    default_n_jobs: ClassVar[int]
    @property
    def supports_return_generator(self) -> bool: ...
    @property
    def supports_timeout(self) -> bool: ...
    nesting_level: int | None
    inner_max_num_threads: int
    def __init__(
        self,
        nesting_level: int | None = ...,
        inner_max_num_threads: int | None = ...,
        **kwargs: Any,
    ) -> None: ...
    MAX_NUM_THREADS_VARS: ClassVar[list[str]]
    TBB_ENABLE_IPC_VAR: ClassVar[str]
    @abstractmethod
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    @abstractmethod
    def apply_async(
        self,
        func: Callable[[], _T],
        callback: Callable[[AnyContainer[_T]], Any]  # FIXME: mypy error
        | None = ...,
    ) -> AnyContainer[_T]: ...
    def retrieve_result_callback(
        self, out: futures.Future[_T] | AsyncResult[_T]
    ) -> _T: ...
    parallel: Parallel[_R]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        **backend_args: Any,
    ) -> int: ...
    def start_call(self) -> None: ...
    def stop_call(self) -> None: ...
    def terminate(self) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def get_exceptions(self) -> list[BaseException]: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def get_nested_backend(
        self,
    ) -> tuple[SequentialBackend[Any] | ThreadingBackend[Any], int | None]: ...
    def retrieval_context(self) -> Generator[None, None, None]: ...
    @staticmethod
    def in_main_thread() -> bool: ...

class SequentialBackend(ParallelBackendBase[_R], Generic[_R]):
    uses_threads: ClassVar[bool]
    supports_timeout: ClassVar[bool]  # pyright: ignore[reportIncompatibleMethodOverride]
    supports_retrieve_callback: ClassVar[bool]
    supports_sharedmem: ClassVar[bool]
    def apply_async(
        self, func: Callable[[], Any], callback: Callable[..., Any] | None = ...
    ) -> NoReturn: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class PoolManagerMixin:
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    def terminate(self) -> None: ...
    def apply_async(
        self,
        func: Callable[[], _T],
        callback: Callable[[AsyncResult[_T]], Any] | None = ...,
    ) -> AsyncResult[_T]: ...
    def retrieve_result_callback(self, out: Any) -> Any: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...

class AutoBatchingMixin(Generic[_R]):
    MIN_IDEAL_BATCH_DURATION: ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: ClassVar[int]
    parallel: Parallel[_R]
    def __init__(self, **kwargs: Any) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def reset_batch_stats(self) -> None: ...

class ThreadingBackend(PoolManagerMixin, ParallelBackendBase[_R], Generic[_R]):
    supports_retrieve_callback: ClassVar[bool]
    uses_threads: ClassVar[bool]
    supports_sharedmem: ClassVar[bool]
    def configure(  # type: ignore[override]
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        **backend_args: Any,
    ) -> int: ...

class MultiprocessingBackend(  # type: ignore[misc] # FIXME
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
        **memmappingpool_args: Any,
    ) -> int: ...

class LokyBackend(AutoBatchingMixin[_R], ParallelBackendBase[_R], Generic[_R]):  # type: ignore[misc] # FIXME
    supports_retrieve_callback: ClassVar[bool]
    supports_inner_max_num_threads: ClassVar[bool]
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
        idle_worker_timeout: float = ...,
        **memmappingexecutor_args: Any,
    ) -> int: ...
    def terminate(self) -> None: ...
    def abort_everything(self, ensure_ready: bool = ...) -> None: ...
    def apply_async(
        self,
        func: Callable[[], _T],
        callback: Callable[[futures.Future[_T]], Any] | None = ...,
    ) -> futures.Future[_T]: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...

class FallbackToBackend(Exception):  # noqa: N818
    backend: ParallelBackendBase[Any]
    def __init__(self, backend: ParallelBackendBase[Any]) -> None: ...

def inside_dask_worker() -> bool: ...
