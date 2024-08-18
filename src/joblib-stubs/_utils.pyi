import ast
from dataclasses import dataclass
from typing import Any, Callable, Generic

from joblib._multiprocessing_helpers import mp as mp
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

operators: dict[ast.AST, Callable[[Any, Any], Any]]

def eval_expr(expr: str) -> Any: ...
def eval_(node: ast.AST) -> Any: ...
@dataclass(frozen=True)
class _Sentinel(Generic[_T]):
    default_value: _T
    def __init__(self, default_value: _T) -> None: ...

class _TracebackCapturingWrapper(Generic[_P, _T]):
    func: Callable[_P, _T]
    def __init__(self, func: Callable[_P, _T]) -> None: ...
    def __call__(self, **kwargs: Any) -> _T: ...
