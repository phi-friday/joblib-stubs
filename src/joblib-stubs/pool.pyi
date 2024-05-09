import typing
from multiprocessing.context import BaseContext
from multiprocessing.pool import Pool
from pickle import Pickler

import typing_extensions
from _typeshed import Incomplete, SupportsWrite

from ._memmapping_reducer import TemporaryResourcesManager as TemporaryResourcesManager
from ._memmapping_reducer import _MmapMode
from ._memmapping_reducer import get_memmapping_reducers as get_memmapping_reducers
from ._multiprocessing_helpers import assert_spawning as assert_spawning
from ._multiprocessing_helpers import mp as mp

WindowsError: type[BaseException | None]

class CustomizablePickler(Pickler):
    dispatch: Incomplete
    dispatch_table: Incomplete
    def __init__(
        self,
        writer: SupportsWrite[bytes],
        reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = None,
        protocol: int = ...,
    ) -> None: ...
    def register[T](
        self,
        type: type[T],  # noqa: A002
        reduce_func: typing.Callable[typing_extensions.Concatenate[T, ...], typing.Any],
    ) -> None: ...

class CustomizablePicklingQueue:
    def __init__(
        self, context: BaseContext, reducers: Incomplete | None = None
    ) -> None: ...
    def empty(self) -> bool: ...

class PicklingPool(Pool):
    def __init__(
        self,
        processes: int | None = None,
        forward_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = None,
        backward_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = None,
        **kwargs: typing.Any,
    ) -> None: ...

class MemmappingPool(PicklingPool):
    def __init__(
        self,
        processes: int | None = None,
        temp_folder: str | None = None,
        max_nbytes: float | None = 1000000.0,
        mmap_mode: _MmapMode = "r",
        forward_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = None,
        backward_reducers: dict[type[typing.Any], typing.Callable[..., typing.Any]]
        | None = None,
        verbose: int = 0,
        context_id: tuple[str, ...] | None = None,
        prewarm: bool | str = False,
        **kwargs: typing.Any,
    ) -> None: ...
    def terminate(self) -> None: ...
