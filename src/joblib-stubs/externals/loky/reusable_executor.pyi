import threading
from concurrent import futures
from multiprocessing.context import BaseContext
from typing import Any, Callable

from _typeshed import Incomplete
from joblib.externals.loky.process_executor import ProcessPoolExecutor
from typing_extensions import ParamSpec, TypeAlias, TypeVar

__all__ = ["get_reusable_executor"]

_T = TypeVar("_T")
_P = ParamSpec("_P")

_Context: TypeAlias = str | BaseContext

def get_reusable_executor(
    max_workers: int | None = ...,
    context: _Context | None = ...,
    timeout: float = ...,
    kill_workers: bool = ...,
    reuse: str = ...,
    job_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
    result_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
    initializer: Callable[..., Any] | None = ...,
    initargs: tuple[Any, ...] = ...,
    env: dict[str, str] | None = ...,
) -> _ReusablePoolExecutor: ...

class _ReusablePoolExecutor(ProcessPoolExecutor):
    executor_id: Incomplete
    def __init__(
        self,
        submit_resize_lock: threading.RLock,
        max_workers: int | None = ...,
        context: _Context | None = ...,
        timeout: float | None = ...,
        executor_id: int = ...,
        job_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
        result_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
        initializer: Callable[..., Any] | None = ...,
        initargs: tuple[Any, ...] = ...,
        env: dict[str, str] | None = ...,
    ) -> None: ...
    @classmethod
    def get_reusable_executor(
        cls,
        max_workers: int | None = ...,
        context: _Context | None = ...,
        timeout: float = ...,
        kill_workers: bool = ...,
        reuse: str = ...,
        job_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
        result_reducers: dict[type[Any], Callable[..., Any]] | None = ...,
        initializer: Callable[..., Any] | None = ...,
        initargs: tuple[Any, ...] = ...,
        env: dict[str, str] | None = ...,
    ) -> _ReusablePoolExecutor: ...
    def submit(
        self, fn: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> futures.Future[_T]: ...
