from collections.abc import Awaitable, Callable
from pickle import Unpickler
from typing import Any, Concatenate, Literal, Protocol, TypeAlias, overload

from joblib.memory import AsyncMemorizedFunc as AsyncMemorizedFunc
from joblib.memory import MemorizedFunc as MemorizedFunc
from typing_extensions import ParamSpec, TypedDict, TypeVar

_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_P = ParamSpec("_P")
_BaseExceptionT = TypeVar("_BaseExceptionT", bound=BaseException)

class AnyContainer(Protocol[_T_co]): ...  # mypy override error

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
    def __call__(
        self,
        func: Callable[_P, Awaitable[_T]],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @overload
    def __call__(
        self,
        func: Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[_P, _T]: ...

RebuildExc: TypeAlias = Callable[[_BaseExceptionT, str], _BaseExceptionT]
WindowsError: type[OSError | None]
DaskTaskItem: TypeAlias = tuple[Callable[_P, _T], list[Any], dict[str, Any]]
DaskScatterIterItem: TypeAlias = list[Any] | dict[Any, Any]
Prefer: TypeAlias = Literal["processes", "threads"]
Require: TypeAlias = Literal["sharedmem"]
HashType: TypeAlias = Literal["md5", "sha1"]
MmapMode: TypeAlias = Literal[
    "readonly", "r", "copyonwrite", "c", "readwrite", "r+", "write", "w+"
]
Reducer: TypeAlias = Callable[Concatenate[type[_T], ...], Any]
Dispatch: TypeAlias = Callable[[Unpickler, _T], None]
ReturnList: TypeAlias = Literal["list"]
ReturnGererator: TypeAlias = Literal["generator"]
ReturnGereratorUnordered: TypeAlias = Literal["generator_unordered"]
ReturnUnknown: TypeAlias = str
ReturnAs: TypeAlias = (
    ReturnList | ReturnGererator | ReturnGereratorUnordered | ReturnUnknown
)
BatchedCall: TypeAlias = tuple[Callable[_P, _T], tuple[Any, ...], dict[str, Any]]
