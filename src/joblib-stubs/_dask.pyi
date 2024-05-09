import typing
import weakref
from collections.abc import Generator
from concurrent import futures

from _typeshed import Incomplete

from .parallel import AutoBatchingMixin as AutoBatchingMixin
from .parallel import ParallelBackendBase as ParallelBackendBase
from .parallel import parallel_config as parallel_config

def is_weakrefable(obj: typing.Any) -> bool: ...

class _WeakKeyDictionary:
    def __init__(self) -> None: ...
    def __getitem__(self, obj: typing.Any) -> typing.Any: ...
    def __setitem__(self, obj: typing.Any, value: typing.Any) -> None: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

class Batch:
    def __init__(self, tasks: Incomplete) -> None: ...
    def __call__(self, tasks: Incomplete | None = None) -> list[typing.Any]: ...

class DaskDistributedBackend(AutoBatchingMixin, ParallelBackendBase):
    MIN_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    supports_retrieve_callback: typing.ClassVar[bool]
    default_n_jobs: typing.ClassVar[int]
    client: Incomplete
    data_futures: dict[int, Incomplete]
    wait_for_workers_timeout: int
    submit_kwargs: dict[str, typing.Any]
    waiting_futures: typing.Iterator[Incomplete]
    def __init__(
        self,
        scheduler_host: Incomplete | None = None,
        scatter: list[Incomplete] | tuple[Incomplete, ...] | None = None,
        client: Incomplete | None = None,
        loop: Incomplete | None = None,
        wait_for_workers_timeout: int = 10,
        **submit_kwargs: typing.Any,
    ) -> None: ...
    def __reduce__(self) -> tuple[type[DaskDistributedBackend], tuple[()]]: ...
    def get_nested_backend(
        self,
    ) -> tuple[DaskDistributedBackend, typing.Literal[-1]]: ...
    parallel: Incomplete
    def configure(
        self,
        n_jobs: int = 1,
        parallel: Incomplete | None = None,
        **backend_args: typing.Any,
    ) -> int: ...
    call_data_futures: weakref.WeakKeyDictionary[typing.Any, typing.Any]
    def start_call(self) -> None: ...
    def stop_call(self) -> None: ...
    def effective_n_jobs(self, n_jobs: typing.Any) -> int: ...
    def apply_async(
        self, func: Incomplete, callback: typing.Callable[..., typing.Any] | None = None
    ) -> futures.Future[typing.Any]: ...
    def retrieve_result_callback(self, out: Incomplete) -> Incomplete: ...
    def abort_everything(self, ensure_ready: bool = True) -> None: ...
    def retrieval_context(self) -> Generator[None, None, None]: ...
