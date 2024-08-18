from types import ModuleType
from typing import Any, BinaryIO

from joblib._typeshed import MmapMode
from joblib.numpy_pickle_utils import Unpickler as Unpickler
from numpy.typing import NDArray

_MAX_LEN: int
_CHUNK_SIZE: int

def hex_str(an_int: int) -> str: ...
def asbytes(s: str | bytes) -> bytes: ...
def read_zfile(file_handle: BinaryIO) -> bytes: ...
def write_zfile(file_handle: BinaryIO, data: bytes, compress: int = ...) -> None: ...

class NDArrayWrapper:
    filename: str
    subclass: type[NDArray[Any]]
    allow_mmap: bool
    def __init__(
        self, filename: str, subclass: NDArray[Any], allow_mmap: bool = ...
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> NDArray[Any]: ...

class ZNDArrayWrapper(NDArrayWrapper):
    filename: str
    state: tuple[Any, ...]
    init_args: tuple[Any, ...]
    def __init__(
        self, filename: str, init_args: tuple[Any, ...], state: tuple[Any, ...]
    ) -> None: ...
    def read(self, unpickler: Unpickler) -> NDArray[Any]: ...

class ZipNumpyUnpickler(Unpickler):
    # dispatch: typing.ClassVar[dict[type[typing.Any], Dispatch[typing.Any]]]  # noqa: ERA001, E501
    mmap_mode: MmapMode
    file_handle: BinaryIO
    np: ModuleType
    def __init__(
        self, filename: str, file_handle: BinaryIO, mmap_mode: MmapMode | None = ...
    ) -> None: ...
    def load_build(self) -> None: ...

def load_compatibility(filename: str) -> Any: ...
