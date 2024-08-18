from pathlib import Path
from types import ModuleType
from typing import Any, BinaryIO, ClassVar, Literal

import numpy as np
from _typeshed import SupportsRead, SupportsWrite
from joblib._typeshed import Dispatch, MmapMode
from joblib.backports import make_memmap as make_memmap
from joblib.compressor import LZ4_NOT_INSTALLED_ERROR as LZ4_NOT_INSTALLED_ERROR
from joblib.compressor import BinaryZlibFile as BinaryZlibFile
from joblib.compressor import BZ2CompressorWrapper as BZ2CompressorWrapper
from joblib.compressor import GzipCompressorWrapper as GzipCompressorWrapper
from joblib.compressor import LZ4CompressorWrapper as LZ4CompressorWrapper
from joblib.compressor import LZMACompressorWrapper as LZMACompressorWrapper
from joblib.compressor import XZCompressorWrapper as XZCompressorWrapper
from joblib.compressor import ZlibCompressorWrapper as ZlibCompressorWrapper
from joblib.compressor import lz4 as lz4  # type: ignore
from joblib.compressor import register_compressor as register_compressor
from joblib.numpy_pickle_compat import NDArrayWrapper as NDArrayWrapper
from joblib.numpy_pickle_compat import ZNDArrayWrapper as ZNDArrayWrapper
from joblib.numpy_pickle_compat import load_compatibility as load_compatibility
from joblib.numpy_pickle_utils import BUFFER_SIZE as BUFFER_SIZE
from joblib.numpy_pickle_utils import Pickler as Pickler
from joblib.numpy_pickle_utils import Unpickler as Unpickler
from numpy.typing import DTypeLike, NDArray

NUMPY_ARRAY_ALIGNMENT_BYTES: int

class NumpyArrayWrapper:
    subclass: type[NDArray[Any]]
    shape: int | tuple[int, ...]
    order: Literal["C", "F"]
    dtype: DTypeLike
    allow_mmap: bool
    numpy_array_alignment_bytes: int
    def __init__(
        self,
        subclass: type[NDArray[Any]],
        shape: int | tuple[int, ...],
        order: Literal["C", "F"],
        dtype: DTypeLike,
        allow_mmap: bool = ...,
        numpy_array_alignment_bytes: bool = ...,
    ) -> None: ...
    def safe_get_numpy_array_alignment_bytes(self) -> Any: ...
    def write_array(self, array: NDArray[Any], pickler: Pickler) -> None: ...
    def read_array(self, unpickler: Unpickler) -> NDArray[Any]: ...
    def read_mmap(self, unpickler: Unpickler) -> np.memmap[Any, Any]: ...
    def read(self, unpickler: Unpickler) -> NDArray[Any]: ...

class NumpyPickler(Pickler):
    dispatch: ClassVar[dict[type[Any], Dispatch[Any]]]
    file_handle: BinaryIO
    buffered: bool
    np: ModuleType
    def __init__(self, fp: BinaryIO, protocol: int | None = ...) -> None: ...
    def save(self, obj: Any) -> None: ...

class NumpyUnpickler(Unpickler):
    # dispatch: typing.ClassVar[dict[type[typing.Any], Dispatch[typing.Any]]]  # noqa: ERA001, E501
    mmap_mode: MmapMode
    file_handle: BinaryIO
    filename: str
    compat_mode: bool
    np: ModuleType
    def __init__(
        self, filename: str, file_handle: BinaryIO, mmap_mode: MmapMode | None = ...
    ) -> None: ...
    def load_build(self) -> None: ...

def dump(
    value: Any,
    filename: str | Path | SupportsWrite[bytes],
    compress: int | bool | tuple[str, int] = ...,
    protocol: int | None = ...,
    cache_size: int | None = ...,
) -> list[str] | None: ...
def load_temporary_memmap(
    filename: str | Path | SupportsRead[bytes],
    mmap_mode: MmapMode,
    unlink_on_gc_collect: bool,
) -> Any: ...
def load(
    filename: str | Path | SupportsRead[bytes], mmap_mode: MmapMode | None = ...
) -> Any: ...
