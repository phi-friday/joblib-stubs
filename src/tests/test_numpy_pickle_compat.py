"""Tests for joblib.numpy_pickle_compat stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.numpy_pickle_compat as mod
from joblib import numpy_pickle_utils


class TestHexStr:
    """Test hex_str function type hints."""

    def test_exists(self) -> None:
        """hex_str should exist in runtime."""
        assert hasattr(mod, "hex_str")
        assert callable(mod.hex_str)

    def test_signature(self) -> None:
        """hex_str should have correct signature."""
        sig = inspect.signature(mod.hex_str)
        params = list(sig.parameters.keys())
        assert params == ["an_int"]

    def test_return_type(self) -> None:
        """hex_str should return str."""
        result = mod.hex_str(255)
        assert_type(result, str)
        assert isinstance(result, str)


class TestAsbytes:
    """Test asbytes function type hints."""

    def test_exists(self) -> None:
        """asbytes should exist in runtime."""
        assert hasattr(mod, "asbytes")
        assert callable(mod.asbytes)

    def test_signature(self) -> None:
        """asbytes should have correct signature."""
        sig = inspect.signature(mod.asbytes)
        params = list(sig.parameters.keys())
        assert params == ["s"]

    def test_return_type(self) -> None:
        """asbytes should return bytes."""
        result = mod.asbytes("test")
        assert_type(result, bytes)
        assert isinstance(result, bytes)


class TestReadZfile:
    """Test read_zfile function type hints."""

    def test_exists(self) -> None:
        """read_zfile should exist in runtime."""
        assert hasattr(mod, "read_zfile")
        assert callable(mod.read_zfile)

    def test_signature(self) -> None:
        """read_zfile should have correct signature."""
        sig = inspect.signature(mod.read_zfile)
        params = list(sig.parameters.keys())
        assert params == ["file_handle"]


class TestWriteZfile:
    """Test write_zfile function type hints."""

    def test_exists(self) -> None:
        """write_zfile should exist in runtime."""
        assert hasattr(mod, "write_zfile")
        assert callable(mod.write_zfile)

    def test_signature(self) -> None:
        """write_zfile should have correct signature."""
        sig = inspect.signature(mod.write_zfile)
        params = list(sig.parameters.keys())
        assert "file_handle" in params
        assert "data" in params
        assert "compress" in params


class TestNDArrayWrapper:
    """Test NDArrayWrapper class type hints."""

    def test_class_exists(self) -> None:
        """NDArrayWrapper should exist in runtime."""
        assert hasattr(mod, "NDArrayWrapper")
        assert inspect.isclass(mod.NDArrayWrapper)

    def test_init_signature(self) -> None:
        """NDArrayWrapper.__init__ should have correct signature."""
        sig = inspect.signature(mod.NDArrayWrapper.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "subclass" in params
        assert "allow_mmap" in params

    def test_read_method(self) -> None:
        """NDArrayWrapper.read should exist."""
        sig = inspect.signature(mod.NDArrayWrapper.read)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params


class TestZNDArrayWrapper:
    """Test ZNDArrayWrapper class type hints."""

    def test_class_exists(self) -> None:
        """ZNDArrayWrapper should exist in runtime."""
        assert hasattr(mod, "ZNDArrayWrapper")
        assert inspect.isclass(mod.ZNDArrayWrapper)

    def test_inherits(self) -> None:
        """ZNDArrayWrapper should inherit from NDArrayWrapper."""
        assert issubclass(mod.ZNDArrayWrapper, mod.NDArrayWrapper)

    def test_init_signature(self) -> None:
        """ZNDArrayWrapper.__init__ should have correct signature."""
        sig = inspect.signature(mod.ZNDArrayWrapper.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "init_args" in params
        assert "state" in params

    def test_read_method(self) -> None:
        """ZNDArrayWrapper.read should exist."""
        sig = inspect.signature(mod.ZNDArrayWrapper.read)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params


class TestZipNumpyUnpickler:
    """Test ZipNumpyUnpickler class type hints."""

    def test_class_exists(self) -> None:
        """ZipNumpyUnpickler should exist in runtime."""
        assert hasattr(mod, "ZipNumpyUnpickler")
        assert inspect.isclass(mod.ZipNumpyUnpickler)

    def test_inherits(self) -> None:
        """ZipNumpyUnpickler should inherit from Unpickler."""
        assert issubclass(mod.ZipNumpyUnpickler, numpy_pickle_utils.Unpickler)

    def test_init_signature(self) -> None:
        """ZipNumpyUnpickler.__init__ should have correct signature."""
        sig = inspect.signature(mod.ZipNumpyUnpickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "file_handle" in params
        assert "mmap_mode" in params

    def test_load_build_method(self) -> None:
        """ZipNumpyUnpickler.load_build should exist."""
        sig = inspect.signature(mod.ZipNumpyUnpickler.load_build)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestLoadCompatibility:
    """Test load_compatibility function type hints."""

    def test_exists(self) -> None:
        """load_compatibility should exist in runtime."""
        assert hasattr(mod, "load_compatibility")
        assert callable(mod.load_compatibility)

    def test_signature(self) -> None:
        """load_compatibility should have correct signature."""
        sig = inspect.signature(mod.load_compatibility)
        params = list(sig.parameters.keys())
        assert params == ["filename"]
