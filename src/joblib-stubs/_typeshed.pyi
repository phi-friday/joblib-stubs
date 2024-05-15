import typing
from pickle import Unpickler

import typing_extensions

_T = typing_extensions.TypeVar("_T")
_T_co = typing_extensions.TypeVar("_T_co", covariant=True)
_P = typing_extensions.ParamSpec("_P")
_BaseExceptionT = typing.TypeVar("_BaseExceptionT", bound=BaseException)

class AnyContainer(typing.Protocol[_T_co]): ...  # mypy override error

class EmptyCellValueClass:
    @classmethod
    def __reduce__(cls) -> str: ...

class Process(typing.Protocol):
    pid: int
    returncode: int | None
    kill: typing.Callable[[], None]
    join: typing.Callable[[], None]

class ItemInfo(typing.TypedDict, total=True):
    location: str

class FullArgSpec(typing.NamedTuple):
    args: list[str]
    varargs: str
    varkw: str
    defaults: tuple[typing.Any, ...]
    kwonlyargs: list[str]
    kwonlydefaults: dict[str, typing.Any] | None
    annotations: dict[str, typing.Any] | None

class ArrayMemmapForwardReducerReduceKwargs(typing.TypedDict, total=True):
    verbose: int
    prewarm: bool

RebuildExc: typing_extensions.TypeAlias = typing.Callable[
    [_BaseExceptionT, str], _BaseExceptionT
]
WindowsError: type[OSError | None]
DaskTaskItem: typing_extensions.TypeAlias = tuple[
    typing.Callable[_P, _T], list[typing.Any], dict[str, typing.Any]
]
DaskScatterIterItem: typing_extensions.TypeAlias = (
    list[typing.Any] | dict[typing.Any, typing.Any]
)
Prefer: typing_extensions.TypeAlias = typing.Literal["processes", "threads"]
Require: typing_extensions.TypeAlias = typing.Literal["sharedmem"]
HashType: typing_extensions.TypeAlias = typing.Literal["md5", "sha1"]
MmapMode: typing_extensions.TypeAlias = typing.Literal["r+", "r", "w+", "c"]
AnyAwaitable: typing_extensions.TypeAlias = (
    typing.Awaitable[_T] | typing.Coroutine[typing.Any, typing.Any, _T]
)
AnyAwaitableCallable: typing_extensions.TypeAlias = (
    typing.Callable[_P, typing.Awaitable[_T]]
    | typing.Callable[_P, typing.Coroutine[typing.Any, typing.Any, _T]]
)
Reducer: typing_extensions.TypeAlias = typing.Callable[
    typing_extensions.Concatenate[type[_T], ...], typing.Any
]
Dispatch: typing_extensions.TypeAlias = typing.Callable[[Unpickler, _T], None]
ReturnList: typing_extensions.TypeAlias = typing.Literal["list"]
ReturnGererator: typing_extensions.TypeAlias = typing.Literal["generator"]
ReturnGereratorUnordered: typing_extensions.TypeAlias = typing.Literal[
    "generator_unordered"
]
ReturnUnknown: typing_extensions.TypeAlias = str
ReturnAs: typing_extensions.TypeAlias = (
    ReturnList | ReturnGererator | ReturnGereratorUnordered | ReturnUnknown
)
BatchedCall: typing_extensions.TypeAlias = tuple[
    typing.Callable[_P, _T], tuple[typing.Any, ...], dict[str, typing.Any]
]
