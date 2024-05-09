import typing
from concurrent import futures

from ._memmapping_reducer import TemporaryResourcesManager as TemporaryResourcesManager
from ._memmapping_reducer import get_memmapping_reducers as get_memmapping_reducers
from .externals.loky.reusable_executor import _ReusablePoolExecutor

def get_memmapping_executor(n_jobs: int, **kwargs: typing.Any) -> futures.Executor: ...

class MemmappingExecutor(_ReusablePoolExecutor):
    @classmethod
    def get_memmapping_executor(
        cls,
        n_jobs: int,
        timeout: int = 300,
        initializer: typing.Callable[..., typing.Any] | None = None,
        initargs: tuple[typing.Any, ...] = (),
        env: typing.Mapping[str, str] | None = None,
        temp_folder: str | None = None,
        context_id: tuple[str, ...] | None = None,
        **backend_args: typing.Any,
    ) -> futures.Executor: ...
    def terminate(self, kill_workers: bool = False) -> None: ...

class _TestingMemmappingExecutor(MemmappingExecutor):
    def apply_async[T](
        self, func: typing.Callable[..., T], args: tuple[typing.Any, ...]
    ) -> futures.Future[T]: ...
    def map[T](
        self, f: typing.Callable[..., T], *args: typing.Iterable[typing.Any]
    ) -> list[T]: ...
