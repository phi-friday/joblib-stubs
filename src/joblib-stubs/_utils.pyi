import ast
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, SupportsAbs

from joblib._multiprocessing_helpers import mp as mp

operators: dict[ast.AST, Callable[[Any, Any], Any]]

def eval_expr(expr: str) -> Any: ...
def limit[F: Callable[..., SupportsAbs[Any]]](
    max_: float | None = ...,
) -> Callable[[F], F]: ...
def eval_(node: ast.AST) -> Any: ...

@dataclass(frozen=True)
class _Sentinel[T]:
    default_value: T
    def __init__(self, default_value: T) -> None: ...

class _TracebackCapturingWrapper[**P, T]:
    func: Callable[P, T]
    def __init__(self, func: Callable[P, T]) -> None: ...
    def __call__(self, **kwargs: Any) -> T: ...
