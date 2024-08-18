from multiprocessing.context import BaseContext
from multiprocessing.queues import Queue as mp_Queue
from multiprocessing.queues import SimpleQueue as mp_SimpleQueue
from queue import Full
from typing import Any, Generic

from joblib._typeshed import Reducer
from typing_extensions import TypeVar

__all__ = ["Queue", "SimpleQueue", "Full"]

_T = TypeVar("_T")

class Queue(mp_Queue[_T], Generic[_T]):
    def __init__(
        self,
        maxsize: int = ...,
        reducers: dict[type[Any], Reducer[Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...

class SimpleQueue(mp_SimpleQueue[_T], Generic[_T]):
    def __init__(
        self,
        reducers: dict[type[Any], Reducer[Any]] | None = ...,
        ctx: BaseContext | None = ...,
    ) -> None: ...
    def close(self) -> None: ...
    def put(self, obj: _T) -> None: ...
