from pickle import Unpickler
from typing import Any, Awaitable, Callable, Coroutine, Literal, NamedTuple, Protocol

from typing_extensions import Concatenate, ParamSpec, TypeAlias, TypedDict, TypeVar

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

class FullArgSpec(NamedTuple):
    args: list[str]
    varargs: str
    varkw: str
    defaults: tuple[Any, ...]
    kwonlyargs: list[str]
    kwonlydefaults: dict[str, Any] | None
    annotations: dict[str, Any] | None

class ArrayMemmapForwardReducerReduceKwargs(TypedDict, total=True):
    verbose: int
    prewarm: bool

RebuildExc: TypeAlias = Callable[[_BaseExceptionT, str], _BaseExceptionT]
WindowsError: type[OSError | None]
DaskTaskItem: TypeAlias = tuple[Callable[_P, _T], list[Any], dict[str, Any]]
DaskScatterIterItem: TypeAlias = list[Any] | dict[Any, Any]
Prefer: TypeAlias = Literal["processes", "threads"]
Require: TypeAlias = Literal["sharedmem"]
HashType: TypeAlias = Literal["md5", "sha1"]
MmapMode: TypeAlias = Literal["r+", "r", "w+", "c"]
AnyAwaitable: TypeAlias = Awaitable[_T] | Coroutine[Any, Any, _T]
AnyAwaitableCallable: TypeAlias = (
    Callable[_P, Awaitable[_T]] | Callable[_P, Coroutine[Any, Any, _T]]
)
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
