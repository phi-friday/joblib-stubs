import types
import typing

import typing_extensions
from joblib._typeshed import FullArgSpec
from joblib.logger import pformat as pformat

_P = typing_extensions.ParamSpec("_P")

full_argspec_fields: str
full_argspec_type = FullArgSpec

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
def format_signature(
    func: typing.Callable[_P, typing.Any], *args: _P.args, **kwargs: _P.kwargs
) -> tuple[list[str], str]: ...
def format_call(
    func: typing.Callable[..., typing.Any],
    args: tuple[typing.Any, ...],
    kwargs: dict[str, typing.Any],
    object_name: str = ...,
) -> str: ...
