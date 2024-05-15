import ast
import typing
from dataclasses import dataclass

import typing_extensions
from joblib._multiprocessing_helpers import mp as mp

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")

operators: dict[ast.AST, typing.Callable[[typing.Any, typing.Any], typing.Any]]

def eval_expr(expr: str) -> typing.Any: ...
def eval_(node: ast.AST) -> typing.Any: ...
@dataclass(frozen=True)
class _Sentinel(typing.Generic[_T]):
    default_value: _T
    def __init__(self, default_value: _T) -> None: ...

class _TracebackCapturingWrapper(typing.Generic[_P, _T]):
    func: typing.Callable[_P, _T]
    def __init__(self, func: typing.Callable[_P, _T]) -> None: ...
    def __call__(self, **kwargs: typing.Any) -> _T: ...
