import typing
import weakref

from _typeshed import Incomplete
from joblib.parallel import AutoBatchingMixin as AutoBatchingMixin
from joblib.parallel import Parallel as Parallel
from joblib.parallel import ParallelBackendBase as ParallelBackendBase
from joblib.parallel import parallel_config as parallel_config

def is_weakrefable(obj: typing.Any) -> bool: ...

class _WeakKeyDictionary:
    def __init__(self) -> None: ...
    def __getitem__(self, obj: typing.Any) -> typing.Any: ...
    def __setitem__(self, obj: typing.Any, value: typing.Any) -> None: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...

class Batch:
    def __init__(self, tasks: Incomplete) -> None: ...
    def __call__(self, tasks: Incomplete | None = ...) -> list[typing.Any]: ...

class DaskDistributedBackend(AutoBatchingMixin, ParallelBackendBase):
    MIN_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    MAX_IDEAL_BATCH_DURATION: typing.ClassVar[float]
    client: Incomplete
    data_futures: dict[int, Incomplete]
    wait_for_workers_timeout: int
    submit_kwargs: dict[str, typing.Any]
    waiting_futures: typing.Iterator[Incomplete]
    def __init__(
        self,
        scheduler_host: Incomplete | None = ...,
        scatter: list[Incomplete] | tuple[Incomplete, ...] | None = ...,
        client: Incomplete | None = ...,
        loop: Incomplete | None = ...,
        wait_for_workers_timeout: int = ...,
        **submit_kwargs: typing.Any,
    ) -> None: ...
    def __reduce__(self) -> tuple[type[DaskDistributedBackend], tuple[()]]: ...
    def get_nested_backend(
        self,
    ) -> tuple[DaskDistributedBackend, typing.Literal[-1]]: ...
    parallel: Parallel
    def configure(
        self,
        n_jobs: int = ...,
        parallel: Parallel | None = ...,
        **backend_args: typing.Any,
    ) -> int: ...
    call_data_futures: weakref.WeakKeyDictionary[typing.Any, typing.Any]
