from collections.abc import Callable
from inspect import FullArgSpec
from types import FunctionType
from typing import Any

from joblib.logger import pformat as pformat

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
def format_signature[**P](
    func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
) -> tuple[list[str], str]: ...
def format_call(
    func: Callable[..., Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    object_name: str = ...,
) -> str: ...
