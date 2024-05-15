import typing
from concurrent.futures import Future as _BaseFuture

import typing_extensions

_T = typing_extensions.TypeVar("_T")

class Future(_BaseFuture[_T], typing.Generic[_T]): ...
