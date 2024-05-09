import io
import pickle
import types
import typing

import typing_extensions

Pickler = pickle.Pickler
type _HashType = typing.Literal["md5", "sha1"]

class _ConsistentSet:
    def __init__(self, set_sequence: typing.Iterable[typing.Hashable]) -> None: ...

class _MyHash:
    args: tuple[typing.Any]
    def __init__(self, *args: typing.Any) -> None: ...

class Hasher(Pickler):
    stream: io.BytesIO
    def __init__(self, hash_name: _HashType = "md5") -> None: ...
    def hash(self, obj: typing.Any, return_digest: bool = True) -> str: ...
    def save(self, obj: typing.Any) -> None: ...
    def memoize(self, obj: typing.Any) -> None: ...
    def save_global(
        self,
        obj: typing.Any,
        name: str | None = None,
        pack: typing.Callable[
            typing_extensions.Concatenate[str | bytes, ...], bytes
        ] = ...,
    ) -> None: ...
    dispatch: dict[type[typing.Any], typing.Callable[..., typing.Any]]
    def save_set(self, set_items: typing.Iterable[typing.Hashable]) -> None: ...

class NumpyHasher(Hasher):
    coerce_mmap: bool
    np: types.ModuleType
    def __init__(
        self, hash_name: _HashType = "md5", coerce_mmap: bool = False
    ) -> None: ...
    def save(self, obj: typing.Any) -> None: ...

def hash(  # noqa: A001
    obj: typing.Any, hash_name: _HashType = "md5", coerce_mmap: bool = False
) -> str: ...
