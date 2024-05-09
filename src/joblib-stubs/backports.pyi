import re

import numpy as np
from _memmapping_reducer import _MmapMode
from _typeshed import StrOrBytesPath

class Version:
    def __init__(self, vstring: str | None = None) -> None: ...
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
    filename: str,
    dtype: str = "uint8",
    mode: _MmapMode = "r+",
    offset: int = 0,
    shape: int | tuple[int, ...] | None = None,
    order: str = "C",
    unlink_on_gc_collect: bool = False,
) -> np.memmap: ...

access_denied_errors: tuple[int, int]

def concurrency_safe_rename(src: StrOrBytesPath, dst: StrOrBytesPath) -> None: ...
