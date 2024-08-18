import weakref
from concurrent import futures
from multiprocessing.pool import AsyncResult as AsyncResult
from typing import Any, Callable, ClassVar, Generic, Iterator, Literal

from dask.distributed import Client as Client
from dask.distributed import Future as Future
from distributed.deploy.cluster import Cluster as Cluster
from joblib._typeshed import DaskScatterIterItem, DaskTaskItem, ReturnAs
from joblib.parallel import AutoBatchingMixin as AutoBatchingMixin
from joblib.parallel import Parallel as Parallel
from joblib.parallel import ParallelBackendBase as ParallelBackendBase
from joblib.parallel import parallel_config as parallel_config
from tornado.ioloop import IOLoop as IOLoop
from typing_extensions import TypeVar

_T = TypeVar("_T")
_R = TypeVar("_R", default=Literal["list"], bound=ReturnAs)

def is_weakrefable(obj: Any) -> bool: ...

class _WeakKeyDictionary:
    def __init__(self) -> None: ...
    def __getitem__(self, obj: Any) -> Any: ...
    def __setitem__(self, obj: Any, value: Any) -> None: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

class Batch(Generic[_T]):
    def __init__(self, tasks: list[DaskTaskItem[..., _T]]) -> None: ...
    def __call__(self, tasks: list[DaskTaskItem[..., _T]] | None = ...) -> list[_T]: ...

class DaskDistributedBackend(
    AutoBatchingMixin[_R], ParallelBackendBase[_R], Generic[_R]
):
    MIN_IDEAL_BATCH_DURATION: ClassVar[float]
    client: Client
    data_futures: dict[int, Future]
    wait_for_workers_timeout: float
    submit_kwargs: dict[str, Any]
    waiting_futures: Iterator[Future]
    def __init__(
        self,
        scheduler_host: str | Cluster | None = ...,
        scatter: DaskScatterIterItem | Any | None = ...,
        client: Client | None = ...,
        loop: IOLoop | None = ...,
        wait_for_workers_timeout: float = ...,
        **submit_kwargs: Any,
    ) -> None: ...
    def __reduce__(self) -> tuple[type[DaskDistributedBackend], tuple[()]]: ...
    def get_nested_backend(  # type: ignore[override]
        self,
    ) -> tuple[DaskDistributedBackend, Literal[-1]]: ...
    parallel: Parallel[_R]
    def configure(  # type: ignore[override]
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        **backend_args: Any,
    ) -> int: ...
    call_data_futures: weakref.WeakKeyDictionary[Any, Any]
    def apply_async(
        self, func: Callable[[], _T], callback: Callable[[_T], Any] | None = ...
    ) -> futures.Future[_T]: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...
