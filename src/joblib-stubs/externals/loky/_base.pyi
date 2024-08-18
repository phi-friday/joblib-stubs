from concurrent.futures import Future as _BaseFuture
from typing import Generic

from typing_extensions import TypeVar

_T = TypeVar("_T")

class Future(_BaseFuture[_T], Generic[_T]): ...
