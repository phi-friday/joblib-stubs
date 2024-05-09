import typing
from abc import ABCMeta, abstractmethod
from collections.abc import Generator
from concurrent import futures

from _typeshed import Incomplete

from ._multiprocessing_helpers import mp as mp
from .executor import get_memmapping_executor as get_memmapping_executor
from .externals.loky import cpu_count as cpu_count
from .externals.loky import process_executor as process_executor
from .externals.loky.process_executor import (
    ShutdownExecutorError as ShutdownExecutorError,
)
from .pool import MemmappingPool as MemmappingPool

class ParallelBackendBase(metaclass=ABCMeta):
    supports_inner_max_num_threads: typing.ClassVar[bool]
    supports_retrieve_callback: typing.ClassVar[bool]
    default_n_jobs: typing.ClassVar[int]
    @property
    def supports_return_generator(self) -> bool: ...
    @property
    def supports_timeout(self) -> bool: ...
    nesting_level: int
    inner_max_num_threads: int
    def __init__(
        self,
        nesting_level: int | None = None,
        inner_max_num_threads: int | None = None,
        **kwargs: typing.Any,
    ) -> None: ...
    MAX_NUM_THREADS_VARS: typing.ClassVar[list[str]]
    TBB_ENABLE_IPC_VAR: typing.ClassVar[str]
    @abstractmethod
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    @abstractmethod
    def apply_async[T](
        self,
        func: typing.Callable[[], T],
        callback: typing.Callable[[T], typing.Any] | None = None,
    ) -> futures.Future[T]: ...
    def retrieve_result_callback(self, out: typing.Any) -> None: ...
    parallel: Incomplete
    def configure(
        self,
        n_jobs: int = 1,
        parallel: bool | None = None,
        prefer: typing.Any | None = None,
        require: typing.Any | None = None,
        **backend_args: typing.Any,
    ) -> int: ...
    def start_call(self) -> None: ...
    def stop_call(self) -> None: ...
    def terminate(self) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def get_exceptions(self) -> list[BaseException]: ...
    def abort_everything(self, ensure_ready: bool = True) -> None: ...
    def get_nested_backend(self) -> tuple[ParallelBackendBase, int | None]: ...
    def retrieval_context(self) -> Generator[None, None, None]: ...
    @staticmethod
    def in_main_thread() -> bool: ...

class SequentialBackend(ParallelBackendBase):
    uses_threads: typing.ClassVar[bool]
    supports_timeout: typing.ClassVar[bool]
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_sharedmem: typing.ClassVar[bool]

class PoolManagerMixin:
    def effective_n_jobs(self, n_jobs: int) -> int: ...
    def terminate(self) -> None: ...
    def apply_async[T](
        self,
        func: typing.Callable[[], T],
        callback: typing.Callable[[T], typing.Any] | None = None,
    ) -> futures.Future[T]: ...
    def retrieve_result_callback(self, out: typing.Any) -> typing.Any: ...
    def abort_everything(self, ensure_ready: bool = True) -> None: ...

class AutoBatchingMixin:
    MIN_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: typing.ClassVar[int]
    def __init__(self, **kwargs: typing.Any) -> None: ...
    def compute_batch_size(self) -> int: ...
    def batch_completed(self, batch_size: int, duration: float) -> None: ...
    def reset_batch_stats(self) -> None: ...

class ThreadingBackend(PoolManagerMixin, ParallelBackendBase):
    supports_retrieve_callback: typing.ClassVar[bool]
    uses_threads: typing.ClassVar[bool]
    supports_sharedmem: typing.ClassVar[bool]
    parallel: bool
    def configure(
        self, n_jobs: int = 1, parallel: bool | None = None, **backend_args: typing.Any
    ) -> int: ...

class MultiprocessingBackend(PoolManagerMixin, AutoBatchingMixin, ParallelBackendBase):
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_return_generator: typing.ClassVar[bool]
    parallel: bool
    def configure(
        self,
        n_jobs: int = 1,
        parallel: bool | None = None,
        prefer: typing.Any | None = None,
        require: typing.Any | None = None,
        **memmappingpool_args: typing.Any,
    ) -> int: ...
    def terminate(self) -> None: ...

class LokyBackend(AutoBatchingMixin, ParallelBackendBase):
    supports_retrieve_callback: typing.ClassVar[bool]
    supports_inner_max_num_threads: typing.ClassVar[bool]
    parallel: bool
    def configure(
        self,
        n_jobs: int = 1,
        parallel: bool | None = None,
        prefer: typing.Any | None = None,
        require: typing.Any | None = None,
        idle_worker_timeout: int = 300,
        **memmappingexecutor_args: typing.Any,
    ) -> int: ...
    def terminate(self) -> None: ...
    def abort_everything(self, ensure_ready: bool = True) -> None: ...

class FallbackToBackend(Exception):  # noqa: N818
    backend: ParallelBackendBase
    def __init__(self, backend: ParallelBackendBase) -> None: ...

def inside_dask_worker() -> bool: ...
