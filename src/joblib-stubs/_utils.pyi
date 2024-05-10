import ast
import typing
from dataclasses import dataclass

from joblib._multiprocessing_helpers import mp as mp

operators: dict[ast.AST, typing.Callable[[typing.Any, typing.Any], typing.Any]]

def eval_expr(expr: str) -> typing.Any: ...
def eval_(node: ast.AST) -> typing.Any: ...
@dataclass(frozen=True)
class _Sentinel[T]:
    default_value: T
    def __init__(self, default_value: T) -> None: ...

class _TracebackCapturingWrapper[**P, T]:
    func: typing.Callable[P, T]
    def __init__(self, func: typing.Callable[P, T]) -> None: ...
    def __call__(self, **kwargs: typing.Any) -> T: ...
