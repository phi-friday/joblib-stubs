import typing

import typing_extensions
from joblib.externals.cloudpickle import dumps as dumps
from joblib.externals.cloudpickle import loads as loads

_T = typing_extensions.TypeVar("_T")
_P = typing_extensions.ParamSpec("_P")

WRAP_CACHE: dict[typing.Any, CloudpickledObjectWrapper[typing.Any]]

class CloudpickledObjectWrapper(typing.Generic[_T]):
    def __init__(self, obj: _T, keep_wrapper: bool = ...) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        typing.Callable[[bytes, bool], CloudpickledObjectWrapper[typing.Any]],
        tuple[bytes, bool],
    ]: ...
    def __getattr__(self, attr: str) -> typing.Any: ...

class CallableObjectWrapper(
    CloudpickledObjectWrapper[typing.Callable[_P, _T]], typing.Generic[_P, _T]
):
    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T: ...

def wrap_non_picklable_objects(
    obj: _T, keep_wrapper: bool = ...
) -> CloudpickledObjectWrapper[_T]: ...
