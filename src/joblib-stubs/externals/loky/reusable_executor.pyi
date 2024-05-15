import threading
import typing
from concurrent import futures
from multiprocessing.context import BaseContext

import typing_extensions
from _typeshed import Incomplete
from joblib.externals.loky.process_executor import ProcessPoolExecutor

__all__ = ["get_reusable_executor"]

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")

_Context: typing_extensions.TypeAlias = str | BaseContext

def get_reusable_executor(
    max_workers: int | None = ...,
    context: _Context | None = ...,
    timeout: float = ...,
    kill_workers: bool = ...,
    reuse: str = ...,
    job_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]] | None = ...,
    result_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
    | None = ...,
    initializer: typing.Callable[..., typing.Any] | None = ...,
    initargs: tuple[typing.Any, ...] = ...,
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
        job_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = ...,
        result_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = ...,
        initializer: typing.Callable[..., typing.Any] | None = ...,
        initargs: tuple[typing.Any, ...] = ...,
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
        job_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = ...,
        result_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = ...,
        initializer: typing.Callable[..., typing.Any] | None = ...,
        initargs: tuple[typing.Any, ...] = ...,
        env: dict[str, str] | None = ...,
    ) -> _ReusablePoolExecutor: ...
    def submit(
        self, fn: typing.Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs
    ) -> futures.Future[_T]: ...
