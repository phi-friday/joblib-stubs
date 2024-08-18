from types import FunctionType
from typing import Any, Callable

from joblib._typeshed import FullArgSpec
from joblib.logger import pformat as pformat
from typing_extensions import ParamSpec

_P = ParamSpec("_P")

full_argspec_fields: str
full_argspec_type = FullArgSpec

def get_func_code(func: FunctionType) -> tuple[str, str, int]: ...
def get_func_name(
    func: Callable[..., Any], resolv_alias: bool = ..., win_characters: bool = ...
) -> tuple[list[str], str]: ...
def filter_args(
    func: Callable[..., Any],
    ignore_lst: list[str],
    args: tuple[Any, ...] = ...,
    kwargs: dict[str, Any] = ...,
) -> dict[str, Any]: ...
def format_signature(
    func: Callable[_P, Any], *args: _P.args, **kwargs: _P.kwargs
) -> tuple[list[str], str]: ...
def format_call(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    object_name: str = ...,
) -> str: ...
