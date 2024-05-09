import typing
from mmap import mmap

import typing_extensions

from .backports import make_memmap as make_memmap
from .disk import delete_folder as delete_folder
from .externals.loky.backend import resource_tracker as resource_tracker
from .numpy_pickle import dump as dump
from .numpy_pickle import load as load
from .numpy_pickle import load_temporary_memmap as load_temporary_memmap

type _MmapMode = typing.Literal["r+", "r", "w+", "c"]

WindowsError: type[typing.Any]
SYSTEM_SHARED_MEM_FS: str
SYSTEM_SHARED_MEM_FS_MIN_SIZE: int
FOLDER_PERMISSIONS: int
FILE_PERMISSIONS: int
JOBLIB_MMAPS: set[str]

def add_maybe_unlink_finalizer(memmap: mmap) -> None: ...
def unlink_file(filename: str) -> None: ...

class _WeakArrayKeyMap:
    def __init__(self) -> None: ...
    def get(self, obj: typing.Any) -> typing.Any: ...
    def set(self, obj: typing.Any, value: typing.Any) -> None: ...

def has_shareable_memory(a: typing.Any) -> typing.Any: ...
def reduce_array_memmap_backward(
    a: typing.Any,
) -> tuple[
    typing.Callable[..., typing.Any], typing_extensions.Unpack[tuple[typing.Any, ...]]
]: ...

class ArrayMemmapForwardReducer:
    verbose: int
    def __init__(
        self,
        max_nbytes: int,
        temp_folder_resolver: typing.Callable[..., typing.Any] | None,
        mmap_mode: _MmapMode,
        unlink_on_gc_collect: bool,
        verbose: int = 0,
        prewarm: bool = True,
    ) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        type[ArrayMemmapForwardReducer],
        tuple[int, None, _MmapMode, bool],
        dict[str, typing.Any],
    ]: ...
    def __call__(
        self, a: typing.Any
    ) -> tuple[
        typing.Callable[..., typing.Any],
        typing_extensions.Unpack[tuple[typing.Any, ...]],
    ]: ...

def get_memmapping_reducers(
    forward_reducers: dict[type[typing.Any], ArrayMemmapForwardReducer] | None = None,
    backward_reducers: dict[type[typing.Any], ArrayMemmapForwardReducer] | None = None,
    temp_folder_resolver: typing.Callable[..., typing.Any] | None = None,
    max_nbytes: float = 1000000.0,
    mmap_mode: _MmapMode = "r",
    verbose: int = 0,
    prewarm: bool = False,
    unlink_on_gc_collect: bool = True,
    **kwargs: typing.Any,
) -> tuple[
    dict[type[typing.Any], ArrayMemmapForwardReducer],
    dict[type[typing.Any], ArrayMemmapForwardReducer],
]: ...

class TemporaryResourcesManager:
    def __init__(
        self, temp_folder_root: str | None = None, context_id: str | None = None
    ) -> None: ...
    def set_current_context(self, context_id: str) -> None: ...
    def register_new_context(self, context_id: str) -> None: ...
    def resolve_temp_folder_name(self) -> str: ...
    def register_folder_finalizer(
        self, pool_subfolder: str, context_id: str
    ) -> None: ...
