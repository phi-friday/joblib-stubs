import io
import pickle
from types import ModuleType
from typing import Any, Callable, Hashable, Iterable

from joblib._typeshed import HashType
from typing_extensions import Concatenate

Pickler = pickle.Pickler

class _ConsistentSet:
    def __init__(self, set_sequence: Iterable[Hashable]) -> None: ...

class _MyHash:
    args: tuple[Any]
    def __init__(self, *args: Any) -> None: ...

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
