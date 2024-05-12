import typing

import numpy as np
import typing_extensions
from _typeshed import StrOrBytesPath
from joblib.backports import make_memmap as make_memmap
from joblib.disk import delete_folder as delete_folder
from joblib.externals.loky.backend import resource_tracker as resource_tracker
from joblib.numpy_pickle import dump as dump
from joblib.numpy_pickle import load as load
from joblib.numpy_pickle import load_temporary_memmap as load_temporary_memmap
from numpy.typing import ArrayLike, NDArray

type _MmapMode = typing.Literal["r+", "r", "w+", "c"]

WindowsError: type[OSError | None]
SYSTEM_SHARED_MEM_FS: str
SYSTEM_SHARED_MEM_FS_MIN_SIZE: int
FOLDER_PERMISSIONS: int
FILE_PERMISSIONS: int
JOBLIB_MMAPS: set[str]

def add_maybe_unlink_finalizer(memmap: np.memmap[typing.Any, typing.Any]) -> None: ...
def unlink_file(filename: StrOrBytesPath) -> None: ...

class _WeakArrayKeyMap:
    def __init__(self) -> None: ...
    def get(self, obj: typing.Any) -> typing.Any: ...
    def set(self, obj: typing.Any, value: typing.Any) -> None: ...

def has_shareable_memory(a: typing.Any) -> bool: ...
def reduce_array_memmap_backward(
    a: np.memmap[typing.Any, typing.Any] | ArrayLike,
) -> tuple[
    typing.Callable[..., np.memmap[typing.Any, typing.Any] | NDArray[typing.Any]],
    typing_extensions.Unpack[tuple[typing.Any, ...]],
]: ...

class _ArrayMemmapForwardReducerReduceKwargs(typing.TypedDict, total=True):
    verbose: int
    prewarm: bool

class ArrayMemmapForwardReducer:
    verbose: int
    def __init__(
        self,
        max_nbytes: int,
        temp_folder_resolver: typing.Callable[..., typing.Any] | None,
        mmap_mode: _MmapMode,
        unlink_on_gc_collect: bool,
        verbose: int = ...,
        prewarm: bool = ...,
    ) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        type[ArrayMemmapForwardReducer],
        tuple[int, None, _MmapMode, bool],
        _ArrayMemmapForwardReducerReduceKwargs,
    ]: ...
    def __call__(
        self, a: typing.Any
    ) -> tuple[
        typing.Callable[..., np.memmap[typing.Any, typing.Any] | NDArray[typing.Any]],
        typing_extensions.Unpack[tuple[typing.Any, ...]],
    ]: ...

def get_memmapping_reducers(
    forward_reducers: dict[type[typing.Any], ArrayMemmapForwardReducer] | None = ...,
    backward_reducers: dict[type[typing.Any], ArrayMemmapForwardReducer] | None = ...,
    temp_folder_resolver: typing.Callable[..., typing.Any] | None = ...,
    max_nbytes: float = ...,
    mmap_mode: _MmapMode = ...,
    verbose: int = ...,
    prewarm: bool = ...,
    unlink_on_gc_collect: bool = ...,
    **kwargs: typing.Any,
) -> tuple[
    dict[type[typing.Any], ArrayMemmapForwardReducer],
    dict[type[typing.Any], ArrayMemmapForwardReducer],
]: ...

class TemporaryResourcesManager:
    def __init__(
        self, temp_folder_root: str | None = ..., context_id: str | None = ...
    ) -> None: ...
    def set_current_context(self, context_id: str) -> None: ...
    def register_new_context(self, context_id: str) -> None: ...
    def resolve_temp_folder_name(self) -> str: ...
    def register_folder_finalizer(
        self, pool_subfolder: str, context_id: str
    ) -> None: ...
