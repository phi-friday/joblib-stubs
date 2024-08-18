# pyright: reportIncompatibleMethodOverride=false
from multiprocessing.context import BaseContext
from typing import Any, Callable, Literal

from joblib._typeshed import Reducer
from joblib.externals.loky.backend.process import (
    LokyInitMainProcess as LokyInitMainProcess,
)
from joblib.externals.loky.backend.process import LokyProcess as LokyProcess
from joblib.externals.loky.backend.queues import Queue as _Queue
from joblib.externals.loky.backend.queues import SimpleQueue as _SimpleQueue
from joblib.externals.loky.backend.synchronize import (
    BoundedSemaphore as _BoundedSemaphore,
)
from joblib.externals.loky.backend.synchronize import Condition as _Condition
from joblib.externals.loky.backend.synchronize import Event as _Event
from joblib.externals.loky.backend.synchronize import Lock as _Lock
from joblib.externals.loky.backend.synchronize import RLock as _RLock
from joblib.externals.loky.backend.synchronize import Semaphore as _Semaphore

_MAX_WINDOWS_WORKERS: int
START_METHODS: list[str]
physical_cores_cache: int | Literal["not found"] | None
_DEFAULT_START_METHOD: str | None

def get_context(method: str | None = ...) -> BaseContext: ...
def set_start_method(method: str, force: bool = ...) -> None: ...
def get_start_method() -> str: ...
def cpu_count(only_physical_cores: bool = ...) -> int: ...

class LokyContext(BaseContext):
    _name: Literal["loky"]
    Process: type[LokyProcess]
    cpu_count: Callable[[bool], int]
    def Queue(  # noqa: N802
        self, maxsize: int = ..., reducers: dict[type[Any], Reducer[Any]] | None = ...
    ) -> _Queue[Any]: ...
    def SimpleQueue(  # noqa: N802
        self, reducers: dict[type[Any], Reducer[Any]] | None = ...
    ) -> _SimpleQueue[Any]: ...
    def Semaphore(self, value: int = ...) -> _Semaphore: ...  # noqa: N802
    def BoundedSemaphore(self, value: int) -> _BoundedSemaphore: ...  # noqa: N802
    def Lock(self) -> _Lock: ...  # noqa: N802
    def RLock(self) -> _RLock: ...  # noqa: N802
    def Condition(self, lock: _Lock | _RLock | None = ...) -> _Condition: ...  # noqa: N802
    def Event(self) -> _Event: ...  # noqa: N802

class LokyInitMainContext(LokyContext):
    Process: type[LokyInitMainProcess]  # pyright: ignore[reportIncompatibleVariableOverride]

ctx_loky: LokyContext
