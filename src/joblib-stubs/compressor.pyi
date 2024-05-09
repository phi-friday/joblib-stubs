import io
import typing
from io import BufferedIOBase as BufferedIOBase

from _typeshed import Incomplete

from .backports import LooseVersion as LooseVersion

LZ4_NOT_INSTALLED_ERROR: str
_COMPRESSORS: dict[str, CompressorWrapper]
_ZFILE_PREFIX: bytes
_ZLIB_PREFIX: bytes
_GZIP_PREFIX: bytes
_BZ2_PREFIX: bytes
_XZ_PREFIX: bytes
_LZMA_PREFIX: bytes
_LZ4_PREFIX: bytes

def register_compressor(
    compressor_name: str, compressor: CompressorWrapper, force: bool = False
) -> None: ...

class CompressorWrapper:
    fileobj_factory: Incomplete
    prefix: bytes
    extension: str
    def __init__(
        self, obj: Incomplete, prefix: bytes = b"", extension: str = ""
    ) -> None: ...
    def compressor_file(
        self, fileobj: Incomplete, compresslevel: int | None = None
    ) -> Incomplete: ...
    def decompressor_file(self, fileobj: Incomplete) -> Incomplete: ...

class BZ2CompressorWrapper(CompressorWrapper): ...
class LZMACompressorWrapper(CompressorWrapper): ...
class XZCompressorWrapper(LZMACompressorWrapper): ...
class LZ4CompressorWrapper(CompressorWrapper): ...

_MODE_CLOSED: typing.Literal[0]
_MODE_READ: typing.Literal[1]
_MODE_READ_EOF: typing.Literal[2]
_MODE_WRITE: typing.Literal[3]
_BUFFER_SIZE: typing.Literal[8192]

class BinaryZlibFile(io.BufferedIOBase):
    wbits: typing.ClassVar[int]
    compresslevel: int
    def __init__(
        self,
        filename: str,
        mode: typing.Literal["rb", "wb"] = "rb",
        compresslevel: int = 3,
    ) -> None: ...
    def close(self) -> None: ...
    @property
    def closed(self) -> bool: ...
    def fileno(self) -> int: ...
    def seekable(self) -> bool: ...
    def readable(self) -> bool: ...
    def writable(self) -> bool: ...
    def read(self, size: int = -1) -> bytes | None: ...
    def readinto(self, b: bytes) -> int: ...
    def write(self, data: bytes) -> int: ...
    def seek(self, offset: int, whence: int = 0) -> int: ...
    def tell(self) -> int: ...

class ZlibCompressorWrapper(CompressorWrapper):
    def __init__(self) -> None: ...

class BinaryGzipFile(BinaryZlibFile):
    wbits: int

class GzipCompressorWrapper(CompressorWrapper):
    def __init__(self) -> None: ...
