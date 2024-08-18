# pyright: reportUnnecessaryTypeIgnoreComment=false
from joblib.externals.loky import (
    wrap_non_picklable_objects as _wrap_non_picklable_objects,
)
from typing_extensions import TypeVar

_T = TypeVar("_T")

def _my_wrap_non_picklable_objects(obj: _T, keep_wrapper: bool = ...) -> _T: ...

if bool():  # noqa: PYI002, UP018
    wrap_non_picklable_objects = _my_wrap_non_picklable_objects
else:
    wrap_non_picklable_objects = _wrap_non_picklable_objects  # type: ignore[assignment]

__all__ = ["wrap_non_picklable_objects"]
