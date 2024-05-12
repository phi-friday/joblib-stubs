import typing
from multiprocessing.context import BaseContext
from multiprocessing.queues import Queue as mp_Queue
from multiprocessing.queues import SimpleQueue as mp_SimpleQueue
from queue import Full

from joblib.pool import _Reducer

__all__ = ["Queue", "SimpleQueue", "Full"]

class Queue[T](mp_Queue[T]):
    def __init__(
        self,
        maxsize: int = ...,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...

class SimpleQueue[T](mp_SimpleQueue[T]):
    def __init__(
        self,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def put(self, obj: T) -> None: ...
