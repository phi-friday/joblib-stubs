import re
from typing import Any, Literal

import numpy as np
from _typeshed import StrOrBytesPath
from joblib._typeshed import MmapMode
from numpy.typing import DTypeLike

class Version:
    def __init__(self, vstring: str | None = ...) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...

class LooseVersion(Version):
    component_re: re.Pattern[str]
    vstring: str
    version: list[str | int]
    def parse(self, vstring: str) -> None: ...

def make_memmap(
    filename: StrOrBytesPath,
    dtype: DTypeLike = ...,
    mode: MmapMode = ...,
    offset: int = ...,
    shape: int | tuple[int, ...] | None = ...,
    order: Literal["K", "A", "C", "F"] = ...,
    unlink_on_gc_collect: bool = ...,
) -> np.memmap[Any, np.dtype[Any]]: ...
def concurrency_safe_rename(src: StrOrBytesPath, dst: StrOrBytesPath) -> None: ...
