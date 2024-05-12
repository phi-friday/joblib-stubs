import types
import typing

from joblib._memmapping_reducer import _MmapMode
from joblib.numpy_pickle_utils import Unpickler as Unpickler
from joblib.pool import _Dispatch as _Dispatch
from numpy.typing import NDArray

_MAX_LEN: int
_CHUNK_SIZE: int

def hex_str(an_int: int) -> str: ...
def asbytes(s: str | bytes) -> bytes: ...
def read_zfile(file_handle: typing.BinaryIO) -> bytes: ...
def write_zfile(
    file_handle: typing.BinaryIO, data: bytes, compress: int = ...
) -> None: ...

class NDArrayWrapper:
    filename: str
    subclass: type[NDArray[typing.Any]]
    allow_mmap: bool
    def __init__(
        self, filename: str, subclass: NDArray[typing.Any], allow_mmap: bool = ...
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> NDArray[typing.Any]: ...

class ZNDArrayWrapper(NDArrayWrapper):
    filename: str
    state: tuple[typing.Any, ...]
    init_args: tuple[typing.Any, ...]
    def __init__(
        self,
        filename: str,
        init_args: tuple[typing.Any, ...],
        state: tuple[typing.Any, ...],
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> NDArray[typing.Any]: ...

class ZipNumpyUnpickler(Unpickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], _Dispatch[typing.Any]]]
    mmap_mode: _MmapMode
    file_handle: typing.BinaryIO
    np: types.ModuleType
    def __init__(
        self,
        filename: str,
        file_handle: typing.BinaryIO,
        mmap_mode: _MmapMode | None = ...,
    ) -> None: ...
    def load_build(self) -> None: ...

def load_compatibility(filename: str) -> typing.Any: ...
