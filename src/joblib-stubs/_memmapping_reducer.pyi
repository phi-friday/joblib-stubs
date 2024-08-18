from typing import Any, Callable

import numpy as np
from _typeshed import StrOrBytesPath
from joblib._typeshed import ArrayMemmapForwardReducerReduceKwargs, MmapMode
from joblib._typeshed import WindowsError as WindowsError
from joblib.backports import make_memmap as make_memmap
from joblib.disk import delete_folder as delete_folder
from joblib.externals.loky.backend import resource_tracker as resource_tracker
from joblib.numpy_pickle import dump as dump
from joblib.numpy_pickle import load as load
from joblib.numpy_pickle import load_temporary_memmap as load_temporary_memmap
from numpy.typing import ArrayLike, NDArray
from typing_extensions import Unpack

SYSTEM_SHARED_MEM_FS: str
SYSTEM_SHARED_MEM_FS_MIN_SIZE: int
FOLDER_PERMISSIONS: int
FILE_PERMISSIONS: int
JOBLIB_MMAPS: set[str]

def add_maybe_unlink_finalizer(memmap: np.memmap[Any, Any]) -> None: ...
def unlink_file(filename: StrOrBytesPath) -> None: ...

class _WeakArrayKeyMap:
    def __init__(self) -> None: ...
    def get(self, obj: Any) -> Any: ...
    def set(self, obj: Any, value: Any) -> None: ...

def has_shareable_memory(a: Any) -> bool: ...
def reduce_array_memmap_backward(
    a: np.memmap[Any, Any] | ArrayLike,
) -> tuple[
    Callable[..., np.memmap[Any, Any] | NDArray[Any]], Unpack[tuple[Any, ...]]
]: ...

class ArrayMemmapForwardReducer:
    verbose: int
    def __init__(
        self,
        max_nbytes: int,
        temp_folder_resolver: Callable[..., Any] | None,
        mmap_mode: MmapMode,
        unlink_on_gc_collect: bool,
        verbose: int = ...,
        prewarm: bool = ...,
    ) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        type[ArrayMemmapForwardReducer],
        tuple[int, None, MmapMode, bool],
        ArrayMemmapForwardReducerReduceKwargs,
    ]: ...
    def __call__(
        self, a: Any
    ) -> tuple[
        Callable[..., np.memmap[Any, Any] | NDArray[Any]], Unpack[tuple[Any, ...]]
    ]: ...

def get_memmapping_reducers(
    forward_reducers: dict[type[Any], ArrayMemmapForwardReducer] | None = ...,
    backward_reducers: dict[type[Any], ArrayMemmapForwardReducer] | None = ...,
    temp_folder_resolver: Callable[..., Any] | None = ...,
    max_nbytes: float = ...,
    mmap_mode: MmapMode = ...,
    verbose: int = ...,
    prewarm: bool = ...,
    unlink_on_gc_collect: bool = ...,
    **kwargs: Any,
) -> tuple[
    dict[type[Any], ArrayMemmapForwardReducer],
    dict[type[Any], ArrayMemmapForwardReducer],
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
