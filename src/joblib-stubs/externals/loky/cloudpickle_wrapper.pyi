from typing import Any, Callable, Generic

from joblib.externals.cloudpickle import dumps as dumps
from joblib.externals.cloudpickle import loads as loads
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

WRAP_CACHE: dict[Any, CloudpickledObjectWrapper[Any]]

class CloudpickledObjectWrapper(Generic[_T]):
    def __init__(self, obj: _T, keep_wrapper: bool = ...) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        Callable[[bytes, bool], CloudpickledObjectWrapper[Any]], tuple[bytes, bool]
    ]: ...
    def __getattr__(self, attr: str) -> Any: ...

class CallableObjectWrapper(
    CloudpickledObjectWrapper[Callable[_P, _T]], Generic[_P, _T]
):
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...

def wrap_non_picklable_objects(
    obj: _T, keep_wrapper: bool = ...
) -> CloudpickledObjectWrapper[_T]: ...
