import types
import typing

from joblib.logger import pformat as pformat

full_argspec_fields: str

class _FullArgSpec(typing.NamedTuple):
    args: list[str]
    varargs: str
    varkw: str
    defaults: tuple[typing.Any, ...]
    kwonlyargs: list[str]
    kwonlydefaults: dict[str, typing.Any] | None
    annotations: dict[str, typing.Any] | None

full_argspec_type = _FullArgSpec

def get_func_code(func: types.FunctionType) -> tuple[str, str, int]: ...
def get_func_name(
    func: typing.Callable[..., typing.Any],
    resolv_alias: bool = ...,
    win_characters: bool = ...,
) -> tuple[list[str], str]: ...
def filter_args(
    func: typing.Callable[..., typing.Any],
    ignore_lst: list[str],
    args: tuple[typing.Any, ...] = ...,
    kwargs: dict[str, typing.Any] = ...,
) -> dict[str, typing.Any]: ...
def format_signature[**P](
    func: typing.Callable[P, typing.Any], *args: P.args, **kwargs: P.kwargs
) -> tuple[list[str], str]: ...
def format_call(
    func: typing.Callable[..., typing.Any],
    args: tuple[typing.Any, ...],
    kwargs: dict[str, typing.Any],
    object_name: str = ...,
) -> str: ...
