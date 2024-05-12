import threading
import typing
import weakref
from concurrent import futures
from concurrent.futures import Executor
from concurrent.futures.process import BrokenProcessPool as _BPPException
from multiprocessing.context import BaseContext

from joblib.externals.loky._base import Future as Future
from joblib.externals.loky.backend import get_context as get_context
from joblib.externals.loky.backend.context import cpu_count as cpu_count
from joblib.externals.loky.backend.queues import Queue as Queue
from joblib.externals.loky.backend.queues import SimpleQueue as SimpleQueue
from joblib.externals.loky.backend.reduction import (
    get_loky_pickler_name as get_loky_pickler_name,
)
from joblib.externals.loky.backend.reduction import set_loky_pickler as set_loky_pickler
from joblib.externals.loky.backend.synchronize import Lock as Lock
from joblib.externals.loky.backend.synchronize import RLock as RLock
from joblib.externals.loky.backend.utils import _Process as _Process
from joblib.externals.loky.backend.utils import (
    get_exitcodes_terminated_worker as get_exitcodes_terminated_worker,
)
from joblib.externals.loky.backend.utils import kill_process_tree as kill_process_tree
from joblib.pool import _Reducer

MAX_DEPTH: int
_CURRENT_DEPTH: int
_MEMORY_LEAK_CHECK_DELAY: float
_MAX_MEMORY_LEAK_SIZE: int
_USE_PSUTIL: bool

type _Lock = Lock | RLock

class _ThreadWakeup:
    def __init__(self) -> None: ...
    def close(self) -> None: ...
    def wakeup(self) -> None: ...
    def clear(self) -> None: ...

class _ExecutorFlags:
    shutdown: bool
    broken: BrokenProcessPool | TerminatedWorkerError | None
    kill_workers: bool
    shutdown_lock: _Lock
    def __init__(self, shutdown_lock: _Lock) -> None: ...
    def flag_as_shutting_down(self, kill_workers: bool | None = ...) -> None: ...
    def flag_as_broken(
        self, broken: BrokenProcessPool | TerminatedWorkerError | None
    ) -> None: ...

_global_shutdown: bool
_global_shutdown_lock: threading.Lock
_threads_wakeups: weakref.WeakKeyDictionary[
    _ExecutorManagerThread, tuple[threading.Lock, _ThreadWakeup | None]
]
process_pool_executor_at_exit: typing.Callable[..., typing.Any] | None
EXTRA_QUEUED_CALLS: int

class _RemoteTraceback(Exception):  # noqa: N818
    tb: str
    def __init__(self, tb: typing.Any = ...) -> None: ...

type _RebuildExc[T: BaseException] = typing.Callable[[T, str], T]

class _ExceptionWithTraceback[T: BaseException]:
    exc: T
    tb: str
    def __init__(self, exc: T) -> None: ...
    def __reduce__(self) -> tuple[_RebuildExc[T], tuple[T, str]]: ...

class _WorkItem[**P, T]:
    future: futures.Future[T]
    fn: typing.Callable[P, T]
    args: tuple[typing.Any, ...]
    kwargs: dict[str, typing.Any]
    def __init__(
        self,
        future: Future[T],
        fn: typing.Callable[P, T],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> None: ...

class _ResultItem[T]:
    work_id: int
    exception: BaseException | None
    result: T | None
    def __init__(
        self,
        work_id: int,
        exception: BaseException | None = ...,
        result: T | None = ...,  # pyright: ignore[reportInvalidTypeVarUse]
    ) -> None: ...

class _CallItem[**P, T]:
    work_id: int
    fn: typing.Callable[P, T]
    args: tuple[typing.Any, ...]
    kwargs: dict[str, typing.Any]
    loky_pickler: str
    def __init__(
        self,
        work_id: int,
        fn: typing.Callable[P, T],
        args: tuple[typing.Any, ...],
        kwargs: dict[str, typing.Any],
    ) -> None: ...
    def __call__(self) -> T: ...

class _SafeQueue[T](Queue[T]):
    thread_wakeup: _ThreadWakeup | None
    pending_work_items: dict[int, _WorkItem[..., T]] | None
    running_work_items: list[int] | None
    def __init__(
        self,
        max_size: int = ...,
        ctx: BaseContext | None = ...,
        pending_work_items: dict[int, _WorkItem[..., T]] | None = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        running_work_items: list[int] | None = ...,
        thread_wakeup: _ThreadWakeup | None = ...,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
    ) -> None: ...

class _ExecutorManagerThread(threading.Thread):
    thread_wakeup: _ThreadWakeup | None
    shutdown_lock: threading.Lock
    executor_reference: weakref.ReferenceType[ProcessPoolExecutor]
    executor_flags: _ExecutorFlags
    processes: dict[int, _Process]
    call_queue: _SafeQueue | None
    result_queue: SimpleQueue | None
    work_ids_queue: Queue[int]
    pending_work_items: dict[int, _WorkItem[..., typing.Any]]
    running_work_items: list[int]
    processes_management_lock: _Lock
    daemon: bool
    def __init__(self, executor: ProcessPoolExecutor) -> None: ...
    def run(self) -> None: ...
    def add_call_item_to_queue(self) -> None: ...
    def wait_result_broken_or_wakeup(
        self,
    ) -> tuple[
        _RemoteTraceback, bool, BrokenProcessPool | TerminatedWorkerError | None
    ]: ...
    def process_result_item(
        self, result_item: int | _WorkItem[..., typing.Any]
    ) -> None: ...
    def is_shutting_down(self) -> bool: ...
    def terminate_broken(
        self, bpe: BrokenProcessPool | TerminatedWorkerError | None
    ) -> None: ...
    def flag_executor_shutting_down(self) -> None: ...
    def kill_workers(self, reason: str = ...) -> None: ...
    def shutdown_workers(self) -> None: ...
    def join_executor_internals(self) -> None: ...
    def get_n_children_alive(self) -> int: ...

class LokyRecursionError(RuntimeError): ...
class BrokenProcessPool(_BPPException): ...
class TerminatedWorkerError(BrokenProcessPool): ...

BrokenExecutor = BrokenProcessPool

class ShutdownExecutorError(RuntimeError): ...

class ProcessPoolExecutor(Executor):
    def __init__(
        self,
        max_workers: int | None = ...,
        job_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        result_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        timeout: float | None = ...,
        context: BaseContext | None = ...,
        initializer: typing.Callable[..., typing.Any] | None = ...,
        initargs: tuple[typing.Any, ...] = ...,
        env: dict[str, str] | None = ...,
    ) -> None: ...
    def submit[**P, T](
        self, fn: typing.Callable[P, T], *args: P.args, **kwargs: P.kwargs
    ) -> futures.Future[T]: ...
    def map[T](
        self,
        fn: typing.Callable[..., T],
        *iterables: typing.Iterable[typing.Any],
        timeout: float | None = ...,
        chunksize: int = ...,
        **kwargs: typing.Any,
    ) -> typing.Generator[T, typing.Any, None]: ...
    def shutdown(self, wait: bool = ..., kill_workers: bool = ...) -> None: ...
