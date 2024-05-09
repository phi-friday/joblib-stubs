import types
import typing

from _typeshed import Incomplete

from ._memmapping_reducer import _MmapMode
from .backports import make_memmap as make_memmap
from .compressor import LZ4_NOT_INSTALLED_ERROR as LZ4_NOT_INSTALLED_ERROR
from .compressor import BinaryZlibFile as BinaryZlibFile
from .compressor import BZ2CompressorWrapper as BZ2CompressorWrapper
from .compressor import GzipCompressorWrapper as GzipCompressorWrapper
from .compressor import LZ4CompressorWrapper as LZ4CompressorWrapper
from .compressor import LZMACompressorWrapper as LZMACompressorWrapper
from .compressor import XZCompressorWrapper as XZCompressorWrapper
from .compressor import ZlibCompressorWrapper as ZlibCompressorWrapper
from .compressor import lz4 as lz4  # type: ignore
from .compressor import register_compressor as register_compressor
from .numpy_pickle_compat import NDArrayWrapper as NDArrayWrapper
from .numpy_pickle_compat import ZNDArrayWrapper as ZNDArrayWrapper
from .numpy_pickle_compat import load_compatibility as load_compatibility
from .numpy_pickle_utils import BUFFER_SIZE as BUFFER_SIZE
from .numpy_pickle_utils import Pickler as Pickler
from .numpy_pickle_utils import Unpickler as Unpickler

NUMPY_ARRAY_ALIGNMENT_BYTES: int

class NumpyArrayWrapper:
    subclass: type[typing.Any]
    shape: int | tuple[int, ...]
    order: typing.Literal["C", "F"]
    dtype: typing.Any
    allow_mmap: bool
    numpy_array_alignment_bytes: int
    def __init__(
        self,
        subclass: type[typing.Any],
        shape: int | tuple[int, ...],
        order: typing.Literal["C", "F"],
        dtype: typing.Any,
        allow_mmap: bool = False,
        numpy_array_alignment_bytes: bool = ...,
    ) -> None: ...
    def safe_get_numpy_array_alignment_bytes(self) -> typing.Any: ...
    def write_array(self, array: typing.Any, pickler: Pickler) -> None: ...
    def read_array(self, unpickler: Unpickler) -> typing.Any: ...
    def read_mmap(self, unpickler: Unpickler) -> typing.Any: ...
    def read(self, unpickler: Unpickler) -> typing.Any: ...

class NumpyPickler(Pickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], typing.Callable[..., typing.Any]]]
    file_handle: typing.BinaryIO
    buffered: bool
    np: Incomplete
    def __init__(self, fp: typing.BinaryIO, protocol: int | None = None) -> None: ...
    def save(self, obj: typing.Any) -> None: ...

class NumpyUnpickler(Unpickler):
    dispatch: typing.ClassVar[dict[type[typing.Any], typing.Callable[..., typing.Any]]]
    mmap_mode: _MmapMode
    file_handle: typing.BinaryIO
    filename: str
    compat_mode: bool
    np: types.ModuleType
    def __init__(
        self,
        filename: str,
        file_handle: typing.BinaryIO,
        mmap_mode: _MmapMode | None = None,
    ) -> None: ...
    def load_build(self) -> None: ...

def dump(
    value: typing.Any,
    filename: str,
    compress: int | bool | tuple[str, int] = 0,
    protocol: int | None = None,
    cache_size: int | None = None,
) -> list[str] | None: ...
def load_temporary_memmap(
    filename: str, mmap_mode: _MmapMode, unlink_on_gc_collect: bool
) -> typing.Any: ...
def load(filename: str, mmap_mode: _MmapMode | None = None) -> typing.Any: ...
