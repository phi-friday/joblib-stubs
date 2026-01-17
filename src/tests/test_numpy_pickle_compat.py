"""Tests for joblib.numpy_pickle_compat stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.numpy_pickle_compat as numpy_pickle_compat_runtime
from joblib.numpy_pickle_compat import (
    NDArrayWrapper,
    ZipNumpyUnpickler,
    ZNDArrayWrapper,
    asbytes,
    hex_str,
    load_compatibility,
    read_zfile,
    write_zfile,
)
from joblib.numpy_pickle_utils import Unpickler


class TestHexStr:
    """Test hex_str function type hints."""

    def test_exists(self) -> None:
        """hex_str should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "hex_str")
        assert callable(numpy_pickle_compat_runtime.hex_str)

    def test_signature(self) -> None:
        """hex_str should have correct signature."""
        sig = inspect.signature(hex_str)
        params = list(sig.parameters.keys())
        assert params == ["an_int"]

    def test_return_type(self) -> None:
        """hex_str should return str."""
        result = hex_str(255)
        assert_type(result, str)
        assert isinstance(result, str)


class TestAsbytes:
    """Test asbytes function type hints."""

    def test_exists(self) -> None:
        """asbytes should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "asbytes")
        assert callable(numpy_pickle_compat_runtime.asbytes)

    def test_signature(self) -> None:
        """asbytes should have correct signature."""
        sig = inspect.signature(asbytes)
        params = list(sig.parameters.keys())
        assert params == ["s"]

    def test_return_type(self) -> None:
        """asbytes should return bytes."""
        result = asbytes("test")
        assert_type(result, bytes)
        assert isinstance(result, bytes)


class TestReadZfile:
    """Test read_zfile function type hints."""

    def test_exists(self) -> None:
        """read_zfile should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "read_zfile")
        assert callable(numpy_pickle_compat_runtime.read_zfile)

    def test_signature(self) -> None:
        """read_zfile should have correct signature."""
        sig = inspect.signature(read_zfile)
        params = list(sig.parameters.keys())
        assert params == ["file_handle"]


class TestWriteZfile:
    """Test write_zfile function type hints."""

    def test_exists(self) -> None:
        """write_zfile should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "write_zfile")
        assert callable(numpy_pickle_compat_runtime.write_zfile)

    def test_signature(self) -> None:
        """write_zfile should have correct signature."""
        sig = inspect.signature(write_zfile)
        params = list(sig.parameters.keys())
        assert "file_handle" in params
        assert "data" in params
        assert "compress" in params


class TestNDArrayWrapper:
    """Test NDArrayWrapper class type hints."""

    def test_class_exists(self) -> None:
        """NDArrayWrapper should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "NDArrayWrapper")
        assert inspect.isclass(numpy_pickle_compat_runtime.NDArrayWrapper)

    def test_init_signature(self) -> None:
        """NDArrayWrapper.__init__ should have correct signature."""
        sig = inspect.signature(NDArrayWrapper.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "subclass" in params
        assert "allow_mmap" in params

    def test_read_method(self) -> None:
        """NDArrayWrapper.read should exist."""
        sig = inspect.signature(NDArrayWrapper.read)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params


class TestZNDArrayWrapper:
    """Test ZNDArrayWrapper class type hints."""

    def test_class_exists(self) -> None:
        """ZNDArrayWrapper should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "ZNDArrayWrapper")
        assert inspect.isclass(numpy_pickle_compat_runtime.ZNDArrayWrapper)

    def test_inherits(self) -> None:
        """ZNDArrayWrapper should inherit from NDArrayWrapper."""
        assert issubclass(ZNDArrayWrapper, NDArrayWrapper)

    def test_init_signature(self) -> None:
        """ZNDArrayWrapper.__init__ should have correct signature."""
        sig = inspect.signature(ZNDArrayWrapper.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "init_args" in params
        assert "state" in params

    def test_read_method(self) -> None:
        """ZNDArrayWrapper.read should exist."""
        sig = inspect.signature(ZNDArrayWrapper.read)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params


class TestZipNumpyUnpickler:
    """Test ZipNumpyUnpickler class type hints."""

    def test_class_exists(self) -> None:
        """ZipNumpyUnpickler should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "ZipNumpyUnpickler")
        assert inspect.isclass(numpy_pickle_compat_runtime.ZipNumpyUnpickler)

    def test_inherits(self) -> None:
        """ZipNumpyUnpickler should inherit from Unpickler."""
        assert issubclass(ZipNumpyUnpickler, Unpickler)

    def test_init_signature(self) -> None:
        """ZipNumpyUnpickler.__init__ should have correct signature."""
        sig = inspect.signature(ZipNumpyUnpickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "file_handle" in params
        assert "mmap_mode" in params

    def test_load_build_method(self) -> None:
        """ZipNumpyUnpickler.load_build should exist."""
        sig = inspect.signature(ZipNumpyUnpickler.load_build)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestLoadCompatibility:
    """Test load_compatibility function type hints."""

    def test_exists(self) -> None:
        """load_compatibility should exist in runtime."""
        assert hasattr(numpy_pickle_compat_runtime, "load_compatibility")
        assert callable(numpy_pickle_compat_runtime.load_compatibility)

    def test_signature(self) -> None:
        """load_compatibility should have correct signature."""
        sig = inspect.signature(load_compatibility)
        params = list(sig.parameters.keys())
        assert params == ["filename"]
