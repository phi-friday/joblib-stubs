from typing_extensions import TypeVar

_T = TypeVar("_T")

def wrap_non_picklable_objects(obj: _T, keep_wrapper: bool = ...) -> _T: ...
