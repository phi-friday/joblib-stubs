import typing

from _typeshed import Incomplete

from ._memmapping_reducer import _MmapMode
from .numpy_pickle_utils import Unpickler as Unpickler

_MAX_LEN: int
_CHUNK_SIZE: int

def hex_str(an_int: int) -> str: ...
def asbytes(s: str | bytes) -> bytes: ...
def read_zfile(file_handle: typing.BinaryIO) -> bytes: ...
def write_zfile(
    file_handle: typing.BinaryIO, data: bytes, compress: int = 1
) -> None: ...

class NDArrayWrapper:
    filename: str
    subclass: type[typing.Any]
    allow_mmap: bool
    def __init__(
        self, filename: str, subclass: type[typing.Any], allow_mmap: bool = True
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> typing.Any: ...

class ZNDArrayWrapper(NDArrayWrapper):
    filename: str
    state: tuple[typing.Any, ...]
    init_args: Incomplete
    def __init__(
        self,
        filename: str,
        init_args: tuple[typing.Any, ...],
        state: tuple[typing.Any, ...],
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> typing.Any: ...

class ZipNumpyUnpickler(Unpickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], typing.Callable[..., typing.Any]]]
    mmap_mode: _MmapMode
    file_handle: typing.BinaryIO
    np: Incomplete
    def __init__(
        self,
        filename: str,
        file_handle: typing.BinaryIO,
        mmap_mode: _MmapMode | None = None,
    ) -> None: ...
    def load_build(self) -> None: ...

def load_compatibility(filename: str) -> typing.Any: ...
