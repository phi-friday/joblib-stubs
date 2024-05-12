import typing
from multiprocessing.context import BaseContext
from multiprocessing.pool import Pool
from pickle import Pickler, Unpickler

import typing_extensions
from _typeshed import SupportsWrite
from joblib._memmapping_reducer import (
    TemporaryResourcesManager as TemporaryResourcesManager,
)
from joblib._memmapping_reducer import WindowsError as WindowsError
from joblib._memmapping_reducer import _MmapMode
from joblib._memmapping_reducer import (
    get_memmapping_reducers as get_memmapping_reducers,
)
from joblib._multiprocessing_helpers import assert_spawning as assert_spawning
from joblib._multiprocessing_helpers import mp as mp

type _Reducer[T] = typing.Callable[
    typing_extensions.Concatenate[type[T], ...], typing.Any
]
type _Dispatch[T] = typing.Callable[[Unpickler, T], None]

class CustomizablePickler(Pickler):
    dispatch: dict[type[typing.Any], _Dispatch[typing.Any]]
    dispatch_table: dict[type[typing.Any], _Reducer[typing.Any]]
    def __init__(
        self,
        writer: SupportsWrite[bytes],
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        protocol: int = ...,
    ) -> None: ...
    def register[T](
        self,
        type: type[T],  # noqa: A002
        reduce_func: _Reducer[T],
    ) -> None: ...

class CustomizablePicklingQueue:
    def __init__(
        self,
        context: BaseContext,
        reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
    ) -> None: ...
    def empty(self) -> bool: ...

class PicklingPool(Pool):
    def __init__(
        self,
        processes: int | None = ...,
        forward_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        backward_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        **kwargs: typing.Any,
    ) -> None: ...

class MemmappingPool(PicklingPool):
    def __init__(
        self,
        processes: int | None = ...,
        temp_folder: str | None = ...,
        max_nbytes: float | None = ...,
        mmap_mode: _MmapMode = ...,
        forward_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        backward_reducers: dict[type[typing.Any], _Reducer[typing.Any]] | None = ...,
        verbose: int = ...,
        context_id: tuple[str, ...] | None = ...,
        prewarm: bool | str = ...,
        **kwargs: typing.Any,
    ) -> None: ...
    def terminate(self) -> None: ...
