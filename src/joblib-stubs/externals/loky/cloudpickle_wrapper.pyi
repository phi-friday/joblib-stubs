import typing

from joblib.externals.cloudpickle import dumps as dumps
from joblib.externals.cloudpickle import loads as loads

WRAP_CACHE: dict[typing.Any, CloudpickledObjectWrapper[typing.Any]]

class CloudpickledObjectWrapper[T]:
    def __init__(self, obj: T, keep_wrapper: bool = ...) -> None: ...
    def __reduce__(
        self,
    ) -> tuple[
        typing.Callable[[bytes, bool], CloudpickledObjectWrapper[typing.Any]],
        tuple[bytes, bool],
    ]: ...
    def __getattr__(self, attr: str) -> typing.Any: ...

class CallableObjectWrapper[**P, T](CloudpickledObjectWrapper[typing.Callable[P, T]]):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: ...

def wrap_non_picklable_objects[T](
    obj: T, keep_wrapper: bool = ...
) -> CloudpickledObjectWrapper[T]: ...
