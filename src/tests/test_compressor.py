"""Tests for joblib.compressor stub types."""

from __future__ import annotations

import bz2
import inspect
import io
import lzma
import tempfile
from pathlib import Path
from typing import assert_type

import joblib.compressor as compressor_runtime
from joblib.compressor import (
    LZ4_NOT_INSTALLED_ERROR,
    BinaryGzipFile,
    BinaryZlibFile,
    BZ2CompressorWrapper,
    CompressorWrapper,
    GzipCompressorWrapper,
    LZ4CompressorWrapper,
    LZMACompressorWrapper,
    XZCompressorWrapper,
    ZlibCompressorWrapper,
    register_compressor,
)


class TestRegisterCompressor:
    """Test register_compressor function type hints."""

    def test_register_compressor_exists(self) -> None:
        """register_compressor function should exist in runtime."""
        assert hasattr(compressor_runtime, "register_compressor")
        assert callable(compressor_runtime.register_compressor)

    def test_register_compressor_signature(self) -> None:
        """register_compressor should have correct parameters."""
        sig = inspect.signature(register_compressor)
        params = list(sig.parameters.keys())

        assert "compressor_name" in params
        assert "compressor" in params
        assert "force" in params

    def test_register_compressor_returns_none(self) -> None:
        """register_compressor should return None."""
        wrapper = ZlibCompressorWrapper()
        # Type check: function returns None
        assert_type(register_compressor("test", wrapper, force=True), None)


class TestCompressorWrapper:
    """Test CompressorWrapper class type hints."""

    def test_compressor_wrapper_class_exists(self) -> None:
        """CompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "CompressorWrapper")
        assert inspect.isclass(compressor_runtime.CompressorWrapper)

    def test_compressor_wrapper_attributes(self) -> None:
        """CompressorWrapper should have expected attributes."""
        wrapper = ZlibCompressorWrapper()
        assert hasattr(wrapper, "fileobj_factory")
        assert hasattr(wrapper, "prefix")
        assert hasattr(wrapper, "extension")

        # Type checks
        assert_type(wrapper.prefix, bytes)
        assert_type(wrapper.extension, str)

        # Runtime checks
        assert isinstance(wrapper.prefix, bytes)
        assert isinstance(wrapper.extension, str)

    def test_compressor_wrapper_init_signature(self) -> None:
        """CompressorWrapper.__init__ should accept correct parameters."""
        sig = inspect.signature(CompressorWrapper.__init__)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "obj" in params
        assert "prefix" in params
        assert "extension" in params

    def test_compressor_wrapper_methods(self) -> None:
        """CompressorWrapper should have file methods."""
        assert hasattr(CompressorWrapper, "compressor_file")
        assert hasattr(CompressorWrapper, "decompressor_file")


class TestBZ2CompressorWrapper:
    """Test BZ2CompressorWrapper class type hints."""

    def test_bz2_compressor_wrapper_exists(self) -> None:
        """BZ2CompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "BZ2CompressorWrapper")
        assert inspect.isclass(compressor_runtime.BZ2CompressorWrapper)

    def test_bz2_compressor_wrapper_inherits(self) -> None:
        """BZ2CompressorWrapper should inherit from CompressorWrapper."""
        assert issubclass(BZ2CompressorWrapper, CompressorWrapper)

    def test_bz2_compressor_wrapper_init_signature(self) -> None:
        """BZ2CompressorWrapper.__init__ should have no additional parameters."""
        sig = inspect.signature(BZ2CompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should only have self parameter
        assert params == ["self"]

    def test_bz2_compressor_wrapper_fileobj_factory(self) -> None:
        """BZ2CompressorWrapper.fileobj_factory should be bz2.BZ2File."""
        wrapper = BZ2CompressorWrapper()
        # Type check
        assert_type(wrapper.fileobj_factory, type[bz2.BZ2File])
        # Runtime check
        assert wrapper.fileobj_factory is bz2.BZ2File


class TestLZMACompressorWrapper:
    """Test LZMACompressorWrapper class type hints."""

    def test_lzma_compressor_wrapper_exists(self) -> None:
        """LZMACompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "LZMACompressorWrapper")
        assert inspect.isclass(compressor_runtime.LZMACompressorWrapper)

    def test_lzma_compressor_wrapper_inherits(self) -> None:
        """LZMACompressorWrapper should inherit from CompressorWrapper."""
        assert issubclass(LZMACompressorWrapper, CompressorWrapper)

    def test_lzma_compressor_wrapper_init_signature(self) -> None:
        """LZMACompressorWrapper.__init__ should have no additional parameters."""
        sig = inspect.signature(LZMACompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should only have self parameter
        assert params == ["self"]

    def test_lzma_compressor_wrapper_fileobj_factory(self) -> None:
        """LZMACompressorWrapper.fileobj_factory should be lzma.LZMAFile."""
        wrapper = LZMACompressorWrapper()
        # Type check
        assert_type(wrapper.fileobj_factory, type[lzma.LZMAFile])
        # Runtime check
        assert wrapper.fileobj_factory is lzma.LZMAFile


class TestXZCompressorWrapper:
    """Test XZCompressorWrapper class type hints."""

    def test_xz_compressor_wrapper_exists(self) -> None:
        """XZCompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "XZCompressorWrapper")
        assert inspect.isclass(compressor_runtime.XZCompressorWrapper)

    def test_xz_compressor_wrapper_inherits(self) -> None:
        """XZCompressorWrapper should inherit from LZMACompressorWrapper."""
        assert issubclass(XZCompressorWrapper, LZMACompressorWrapper)

    def test_xz_compressor_wrapper_init_signature(self) -> None:
        """XZCompressorWrapper should inherit __init__ from parent."""
        # XZ doesn't define __init__, so it inherits from LZMA
        sig = inspect.signature(XZCompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should inherit parent's signature (self only)
        assert params == ["self"]


class TestLZ4CompressorWrapper:
    """Test LZ4CompressorWrapper class type hints."""

    def test_lz4_compressor_wrapper_exists(self) -> None:
        """LZ4CompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "LZ4CompressorWrapper")
        assert inspect.isclass(compressor_runtime.LZ4CompressorWrapper)

    def test_lz4_compressor_wrapper_inherits(self) -> None:
        """LZ4CompressorWrapper should inherit from CompressorWrapper."""
        assert issubclass(LZ4CompressorWrapper, CompressorWrapper)

    def test_lz4_compressor_wrapper_init_signature(self) -> None:
        """LZ4CompressorWrapper.__init__ should have no additional parameters."""
        sig = inspect.signature(LZ4CompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should only have self parameter
        assert params == ["self"]


class TestBinaryZlibFile:
    """Test BinaryZlibFile class type hints."""

    def test_binary_zlib_file_exists(self) -> None:
        """BinaryZlibFile class should exist in runtime."""
        assert hasattr(compressor_runtime, "BinaryZlibFile")
        assert inspect.isclass(compressor_runtime.BinaryZlibFile)

    def test_binary_zlib_file_inherits(self) -> None:
        """BinaryZlibFile should inherit from io.BufferedIOBase."""
        assert issubclass(BinaryZlibFile, io.BufferedIOBase)

    def test_binary_zlib_file_has_wbits(self) -> None:
        """BinaryZlibFile should have wbits class variable."""
        assert hasattr(BinaryZlibFile, "wbits")
        # Type check
        assert_type(BinaryZlibFile.wbits, int)
        # Runtime check
        assert isinstance(BinaryZlibFile.wbits, int)

    def test_binary_zlib_file_init_signature(self) -> None:
        """BinaryZlibFile.__init__ should accept correct parameters."""
        sig = inspect.signature(BinaryZlibFile.__init__)
        params = list(sig.parameters.keys())

        assert "self" in params
        assert "filename" in params
        assert "mode" in params
        assert "compresslevel" in params

    def test_binary_zlib_file_attributes(self) -> None:
        """BinaryZlibFile instance should have compresslevel attribute."""
        # Create a temporary file-like object
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name

        try:
            zfile = BinaryZlibFile(tmp_name, mode="wb", compresslevel=6)
            assert hasattr(zfile, "compresslevel")
            # Type check
            assert_type(zfile.compresslevel, int)
            # Runtime check
            assert isinstance(zfile.compresslevel, int)
            zfile.close()
        finally:
            if Path(tmp_name).exists():
                Path(tmp_name).unlink()

    def test_binary_zlib_file_methods(self) -> None:
        """BinaryZlibFile should have expected methods."""
        methods = [
            "close",
            "closed",
            "fileno",
            "seekable",
            "readable",
            "writable",
            "read",
            "readinto",
            "write",
            "seek",
            "tell",
        ]
        for method in methods:
            assert hasattr(BinaryZlibFile, method)

    def test_binary_zlib_file_closed_property(self) -> None:
        """BinaryZlibFile.closed should be a bool property."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_name = tmp.name

        try:
            zfile = BinaryZlibFile(tmp_name, mode="wb")
            # Type check
            assert_type(zfile.closed, bool)
            # Runtime check
            assert isinstance(zfile.closed, bool)
            zfile.close()
            assert zfile.closed is True
        finally:
            if Path(tmp_name).exists():
                Path(tmp_name).unlink()


class TestZlibCompressorWrapper:
    """Test ZlibCompressorWrapper class type hints."""

    def test_zlib_compressor_wrapper_exists(self) -> None:
        """ZlibCompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "ZlibCompressorWrapper")
        assert inspect.isclass(compressor_runtime.ZlibCompressorWrapper)

    def test_zlib_compressor_wrapper_inherits(self) -> None:
        """ZlibCompressorWrapper should inherit from CompressorWrapper."""
        assert issubclass(ZlibCompressorWrapper, CompressorWrapper)

    def test_zlib_compressor_wrapper_init_signature(self) -> None:
        """ZlibCompressorWrapper.__init__ should have no additional parameters."""
        sig = inspect.signature(ZlibCompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should only have self parameter
        assert params == ["self"]

    def test_zlib_compressor_wrapper_fileobj_factory(self) -> None:
        """ZlibCompressorWrapper.fileobj_factory should be BinaryZlibFile."""
        wrapper = ZlibCompressorWrapper()
        # Type check
        assert_type(wrapper.fileobj_factory, type[BinaryZlibFile])
        # Runtime check
        assert wrapper.fileobj_factory is BinaryZlibFile


class TestBinaryGzipFile:
    """Test BinaryGzipFile class type hints."""

    def test_binary_gzip_file_exists(self) -> None:
        """BinaryGzipFile class should exist in runtime."""
        assert hasattr(compressor_runtime, "BinaryGzipFile")
        assert inspect.isclass(compressor_runtime.BinaryGzipFile)

    def test_binary_gzip_file_inherits(self) -> None:
        """BinaryGzipFile should inherit from BinaryZlibFile."""
        assert issubclass(BinaryGzipFile, BinaryZlibFile)

    def test_binary_gzip_file_init_signature(self) -> None:
        """BinaryGzipFile should inherit __init__ from parent."""
        # BinaryGzipFile doesn't define __init__, so it inherits from BinaryZlibFile
        sig = inspect.signature(BinaryGzipFile.__init__)
        params = list(sig.parameters.keys())
        # Should inherit parent's signature
        expected_params = ["self", "filename", "mode", "compresslevel"]
        assert params == expected_params


class TestGzipCompressorWrapper:
    """Test GzipCompressorWrapper class type hints."""

    def test_gzip_compressor_wrapper_exists(self) -> None:
        """GzipCompressorWrapper class should exist in runtime."""
        assert hasattr(compressor_runtime, "GzipCompressorWrapper")
        assert inspect.isclass(compressor_runtime.GzipCompressorWrapper)

    def test_gzip_compressor_wrapper_inherits(self) -> None:
        """GzipCompressorWrapper should inherit from CompressorWrapper."""
        assert issubclass(GzipCompressorWrapper, CompressorWrapper)

    def test_gzip_compressor_wrapper_init_signature(self) -> None:
        """GzipCompressorWrapper.__init__ should have no additional parameters."""
        sig = inspect.signature(GzipCompressorWrapper.__init__)
        params = list(sig.parameters.keys())
        # Should only have self parameter
        assert params == ["self"]

    def test_gzip_compressor_wrapper_fileobj_factory(self) -> None:
        """GzipCompressorWrapper.fileobj_factory should be BinaryGzipFile."""
        wrapper = GzipCompressorWrapper()
        # Type check
        assert_type(wrapper.fileobj_factory, type[BinaryGzipFile])
        # Runtime check
        assert wrapper.fileobj_factory is BinaryGzipFile


class TestLZ4NotInstalledError:
    """Test LZ4_NOT_INSTALLED_ERROR constant."""

    def test_lz4_not_installed_error_exists(self) -> None:
        """LZ4_NOT_INSTALLED_ERROR constant should exist in runtime."""
        assert hasattr(compressor_runtime, "LZ4_NOT_INSTALLED_ERROR")

    def test_lz4_not_installed_error_is_str(self) -> None:
        """LZ4_NOT_INSTALLED_ERROR should be a str."""
        # Type check
        assert_type(LZ4_NOT_INSTALLED_ERROR, str)
        # Runtime check
        assert isinstance(LZ4_NOT_INSTALLED_ERROR, str)
