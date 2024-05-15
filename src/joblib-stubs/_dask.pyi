import typing
import weakref
from concurrent import futures
from multiprocessing.pool import AsyncResult as AsyncResult

import typing_extensions
from dask.distributed import Client as Client
from dask.distributed import Future as Future
from distributed.deploy.cluster import Cluster as Cluster
from joblib.parallel import AutoBatchingMixin as AutoBatchingMixin
from joblib.parallel import Parallel as Parallel
from joblib.parallel import ParallelBackendBase as ParallelBackendBase
from joblib.parallel import _ReturnAs as _ReturnAs
from joblib.parallel import parallel_config as parallel_config
from tornado.ioloop import IOLoop as IOLoop

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")
_R = typing_extensions.TypeVar(
    "_R",
    default=typing.Literal["list"],
    bound="_ReturnAs",  # noqa: PYI020
)

def is_weakrefable(obj: typing.Any) -> bool: ...

class _WeakKeyDictionary:
    def __init__(self) -> None: ...
    def __getitem__(self, obj: typing.Any) -> typing.Any: ...
    def __setitem__(self, obj: typing.Any, value: typing.Any) -> None: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

_TaskItem: typing_extensions.TypeAlias = tuple[
    typing.Callable[_P, _T], list[typing.Any], dict[str, typing.Any]
]

class Batch(typing.Generic[_T]):
    def __init__(self, tasks: list[_TaskItem[..., _T]]) -> None: ...
    def __call__(self, tasks: list[_TaskItem[..., _T]] | None = ...) -> list[_T]: ...

_ScatterIterItem: typing_extensions.TypeAlias = (
    list[typing.Any] | dict[typing.Any, typing.Any]
)

class DaskDistributedBackend(
    AutoBatchingMixin[_R], ParallelBackendBase[_R], typing.Generic[_R]
):
    MIN_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    client: Client
    data_futures: dict[int, Future]
    wait_for_workers_timeout: float
    submit_kwargs: dict[str, typing.Any]
    waiting_futures: typing.Iterator[Future]
    def __init__(
        self,
        scheduler_host: str | Cluster | None = ...,
        scatter: _ScatterIterItem | typing.Any | None = ...,
        client: Client | None = ...,
        loop: IOLoop | None = ...,
        wait_for_workers_timeout: float = ...,
        **submit_kwargs: typing.Any,
    ) -> None: ...
    def __reduce__(self) -> tuple[type[DaskDistributedBackend], tuple[()]]: ...
    def get_nested_backend(  # type: ignore[override]
        self,
    ) -> tuple[DaskDistributedBackend, typing.Literal[-1]]: ...
    parallel: Parallel[_R]
    def configure(  # type: ignore[override]
        self,
        n_jobs: int = ...,
        parallel: Parallel[_R] | None = ...,
        **backend_args: typing.Any,
    ) -> int: ...
    call_data_futures: weakref.WeakKeyDictionary[typing.Any, typing.Any]
    def apply_async(
        self,
        func: typing.Callable[[], _T],
        callback: typing.Callable[[_T], typing.Any] | None = ...,
    ) -> futures.Future[_T]: ...
    # mypy
    def effective_n_jobs(self, n_jobs: int) -> int: ...
