import typing
from multiprocessing.context import BaseContext
from multiprocessing.queues import Queue as mp_Queue
from multiprocessing.queues import SimpleQueue as mp_SimpleQueue
from queue import Full

import typing_extensions
from joblib.pool import _Reducer

__all__ = ["Queue", "SimpleQueue", "Full"]

_T = typing_extensions.TypeVar("_T")

class Queue(mp_Queue[_T], typing.Generic[_T]):
    def __init__(
        self,
        maxsize: int = ...,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...

class SimpleQueue(mp_SimpleQueue[_T], typing.Generic[_T]):
    def __init__(
        self,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def put(self, obj: _T) -> None: ...
