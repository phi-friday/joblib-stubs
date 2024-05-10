from joblib.externals.loky import (
    wrap_non_picklable_objects as _wrap_non_picklable_objects,
)

def _my_wrap_non_picklable_objects[T](obj: T, keep_wrapper: bool = ...) -> T: ...

if bool():  # noqa: PYI002, UP018
    wrap_non_picklable_objects = _my_wrap_non_picklable_objects
else:
    wrap_non_picklable_objects = _wrap_non_picklable_objects

__all__ = ["wrap_non_picklable_objects"]
