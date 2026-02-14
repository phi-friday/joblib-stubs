from collections.abc import Awaitable, Callable
from pickle import Unpickler
from typing import Any, Concatenate, Literal, Protocol, overload

from joblib.memory import AsyncMemorizedFunc as AsyncMemorizedFunc
from joblib.memory import MemorizedFunc as MemorizedFunc
from typing_extensions import TypedDict

class AnyContainer[T](Protocol): ...  # mypy override error

class EmptyCellValueClass:
    @classmethod
    def __reduce__(cls) -> str: ...  # pyright: ignore[reportIncompatibleMethodOverride]

class Process(Protocol):
    pid: int
    returncode: int | None
    kill: Callable[[], None]
    join: Callable[[], None]

class ItemInfo(TypedDict, total=True):
    location: str

class ArrayMemmapForwardReducerReduceKwargs(TypedDict, total=True):
    verbose: int
    prewarm: bool

class MemoryCacheFunc(Protocol):
    @overload
    def __call__(
        self,
        func: None,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemoryCacheFunc: ...
    @overload
    def __call__[**P, T](
        self,
        func: Callable[P, Awaitable[T]],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[P, T]: ...
    @overload
    def __call__[**P, T](
        self,
        func: Callable[P, T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[P, T]: ...

type RebuildExc[_BaseExceptionT: BaseException] = Callable[
    [_BaseExceptionT, str], _BaseExceptionT
]
WindowsError: type[OSError | None]
type DaskTaskItem[**_P, _T] = tuple[Callable[_P, _T], list[Any], dict[str, Any]]
type DaskScatterIterItem = list[Any] | dict[Any, Any]
type Prefer = Literal["processes", "threads"]
type Require = Literal["sharedmem"]
type HashType = Literal["md5", "sha1"]
type MmapMode = Literal[
    "readonly", "r", "copyonwrite", "c", "readwrite", "r+", "write", "w+"
]
type Reducer[_T] = Callable[Concatenate[type[_T], ...], Any]
type Dispatch[_T] = Callable[[Unpickler, _T], None]
type ReturnList = Literal["list"]
type ReturnGererator = Literal["generator"]
type ReturnGereratorUnordered = Literal["generator_unordered"]
type ReturnUnknown = str
type ReturnAs = ReturnList | ReturnGererator | ReturnGereratorUnordered | ReturnUnknown
type BatchedCall[**_P, _T] = tuple[Callable[_P, _T], tuple[Any, ...], dict[str, Any]]
