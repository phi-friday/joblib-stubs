import io
import pickle
from collections.abc import Callable, Hashable, Iterable
from types import ModuleType
from typing import Any, Concatenate

from joblib._typeshed import HashType

Pickler = pickle._Pickler  # noqa: SLF001

class Hasher(Pickler):
    stream: io.BytesIO
    def __init__(self, hash_name: HashType = ...) -> None: ...
    def hash(self, obj: Any, return_digest: bool = ...) -> str: ...
    def save(self, obj: Any) -> None: ...
    def memoize(self, obj: Any) -> None: ...
    def save_global(
        self,
        obj: Any,
        name: str | None = ...,
        pack: Callable[Concatenate[str | bytes, ...], bytes] = ...,
    ) -> None: ...
    # dispatch: dict[type[typing.Any], _Dispatch[typing.Any]]  # noqa: ERA001
    def save_set(self, set_items: Iterable[Hashable]) -> None: ...

class NumpyHasher(Hasher):
    coerce_mmap: bool
    np: ModuleType
    def __init__(self, hash_name: HashType = ..., coerce_mmap: bool = ...) -> None: ...
    def save(self, obj: Any) -> None: ...

def hash(  # noqa: A001
    obj: Any, hash_name: HashType = ..., coerce_mmap: bool = ...
) -> str: ...
