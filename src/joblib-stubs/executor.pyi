import typing
from concurrent import futures

import typing_extensions
from joblib._memmapping_reducer import (
    TemporaryResourcesManager as TemporaryResourcesManager,
)
from joblib._memmapping_reducer import (
    get_memmapping_reducers as get_memmapping_reducers,
)
from joblib.externals.loky.reusable_executor import _ReusablePoolExecutor

_T = typing_extensions.TypeVar("_T")

def get_memmapping_executor(n_jobs: int, **kwargs: typing.Any) -> futures.Executor: ...

class MemmappingExecutor(_ReusablePoolExecutor):
    @classmethod
    def get_memmapping_executor(
        cls,
        n_jobs: int,
        timeout: float = ...,
        initializer: typing.Callable[..., typing.Any] | None = ...,
        initargs: tuple[typing.Any, ...] = ...,
        env: dict[str, str] | None = ...,
        temp_folder: str | None = ...,
        context_id: tuple[str, ...] | None = ...,
        **backend_args: typing.Any,
    ) -> futures.Executor: ...
    def terminate(self, kill_workers: bool = ...) -> None: ...

class _TestingMemmappingExecutor(MemmappingExecutor):
    def apply_async(
        self, func: typing.Callable[..., _T], args: tuple[typing.Any, ...]
    ) -> futures.Future[_T]: ...
    def map(
        self, f: typing.Callable[..., _T], *args: typing.Iterable[typing.Any]
    ) -> list[_T]: ...
