import types
import typing
from pathlib import Path

import numpy as np
from _typeshed import SupportsRead, SupportsWrite
from joblib._memmapping_reducer import _MmapMode
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
from joblib.pool import _Dispatch as _Dispatch
from numpy.typing import DTypeLike, NDArray

NUMPY_ARRAY_ALIGNMENT_BYTES: int

class NumpyArrayWrapper:
    subclass: type[NDArray[typing.Any]]
    shape: int | tuple[int, ...]
    order: typing.Literal["C", "F"]
    dtype: DTypeLike
    allow_mmap: bool
    numpy_array_alignment_bytes: int
    def __init__(
        self,
        subclass: type[NDArray[typing.Any]],
        shape: int | tuple[int, ...],
        order: typing.Literal["C", "F"],
        dtype: DTypeLike,
        allow_mmap: bool = ...,
        numpy_array_alignment_bytes: bool = ...,
    ) -> None: ...
    def safe_get_numpy_array_alignment_bytes(self) -> typing.Any: ...
    def write_array(self, array: NDArray[typing.Any], pickler: Pickler) -> None: ...
    def read_array(self, unpickler: Unpickler) -> NDArray[typing.Any]: ...
    def read_mmap(self, unpickler: Unpickler) -> np.memmap[typing.Any, typing.Any]: ...
    def read(self, unpickler: Unpickler) -> NDArray[typing.Any]: ...

class NumpyPickler(Pickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], _Dispatch[typing.Any]]]
    file_handle: typing.BinaryIO
    buffered: bool
    np: types.ModuleType
    def __init__(self, fp: typing.BinaryIO, protocol: int | None = ...) -> None: ...
    def save(self, obj: typing.Any) -> None: ...

class NumpyUnpickler(Unpickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], _Dispatch[typing.Any]]]
    mmap_mode: _MmapMode
    file_handle: typing.BinaryIO
    filename: str
    compat_mode: bool
    np: types.ModuleType
    def __init__(
        self,
        filename: str,
        file_handle: typing.BinaryIO,
        mmap_mode: _MmapMode | None = ...,
    ) -> None: ...
    def load_build(self) -> None: ...

def dump(
    value: typing.Any,
    filename: str | Path | SupportsWrite[bytes],
    compress: int | bool | tuple[str, int] = ...,
    protocol: int | None = ...,
    cache_size: int | None = ...,
) -> list[str] | None: ...
def load_temporary_memmap(
    filename: str | Path | SupportsRead[bytes],
    mmap_mode: _MmapMode,
    unlink_on_gc_collect: bool,
) -> typing.Any: ...
def load(
    filename: str | Path | SupportsRead[bytes], mmap_mode: _MmapMode | None = ...
) -> typing.Any: ...
