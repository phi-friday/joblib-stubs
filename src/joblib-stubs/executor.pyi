from concurrent import futures
from typing import Any, Callable, Iterable

from joblib._memmapping_reducer import (
    TemporaryResourcesManager as TemporaryResourcesManager,
)
from joblib._memmapping_reducer import (
    get_memmapping_reducers as get_memmapping_reducers,
)
from joblib.externals.loky.reusable_executor import _ReusablePoolExecutor
from typing_extensions import TypeVar

_T = TypeVar("_T")

def get_memmapping_executor(n_jobs: int, **kwargs: Any) -> futures.Executor: ...

class MemmappingExecutor(_ReusablePoolExecutor):
    @classmethod
    def get_memmapping_executor(
        cls,
        n_jobs: int,
        timeout: float = ...,
        initializer: Callable[..., Any] | None = ...,
        initargs: tuple[Any, ...] = ...,
        env: dict[str, str] | None = ...,
        temp_folder: str | None = ...,
        context_id: tuple[str, ...] | None = ...,
        **backend_args: Any,
    ) -> futures.Executor: ...
    def terminate(self, kill_workers: bool = ...) -> None: ...

class _TestingMemmappingExecutor(MemmappingExecutor):
    def apply_async(
        self, func: Callable[..., _T], args: tuple[Any, ...]
    ) -> futures.Future[_T]: ...
    def map(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, f: Callable[..., _T], *args: Iterable[Any]
    ) -> list[_T]: ...
