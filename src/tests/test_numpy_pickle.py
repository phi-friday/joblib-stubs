"""Tests for joblib.numpy_pickle stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.numpy_pickle as mod
from joblib import numpy_pickle_utils


class TestConstants:
    """Test module-level constants."""

    def test_numpy_array_alignment_bytes_exists(self) -> None:
        """NUMPY_ARRAY_ALIGNMENT_BYTES should exist in runtime."""
        assert hasattr(mod, "NUMPY_ARRAY_ALIGNMENT_BYTES")

    def test_numpy_array_alignment_bytes_type(self) -> None:
        """NUMPY_ARRAY_ALIGNMENT_BYTES should be an int."""
        assert_type(mod.NUMPY_ARRAY_ALIGNMENT_BYTES, int)
        assert isinstance(mod.NUMPY_ARRAY_ALIGNMENT_BYTES, int)


class TestNumpyArrayWrapper:
    """Test NumpyArrayWrapper class type hints."""

    def test_class_exists(self) -> None:
        """NumpyArrayWrapper should exist in runtime."""
        assert hasattr(mod, "NumpyArrayWrapper")
        assert inspect.isclass(mod.NumpyArrayWrapper)

    def test_init_signature(self) -> None:
        """NumpyArrayWrapper.__init__ should have correct signature."""
        sig = inspect.signature(mod.NumpyArrayWrapper.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "subclass" in params
        assert "shape" in params
        assert "order" in params
        assert "dtype" in params
        assert "allow_mmap" in params
        assert "numpy_array_alignment_bytes" in params

    def test_safe_get_numpy_array_alignment_bytes_method(self) -> None:
        """NumpyArrayWrapper.safe_get_numpy_array_alignment_bytes should exist."""
        method = mod.NumpyArrayWrapper.safe_get_numpy_array_alignment_bytes
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_write_array_method(self) -> None:
        """NumpyArrayWrapper.write_array should exist."""
        sig = inspect.signature(mod.NumpyArrayWrapper.write_array)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "array" in params
        assert "pickler" in params

    def test_read_array_method(self) -> None:
        """NumpyArrayWrapper.read_array should exist."""
        sig = inspect.signature(mod.NumpyArrayWrapper.read_array)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params
        assert "ensure_native_byte_order" in params

    def test_read_mmap_method(self) -> None:
        """NumpyArrayWrapper.read_mmap should exist."""
        sig = inspect.signature(mod.NumpyArrayWrapper.read_mmap)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params

    def test_read_method(self) -> None:
        """NumpyArrayWrapper.read should exist."""
        sig = inspect.signature(mod.NumpyArrayWrapper.read)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "unpickler" in params
        assert "ensure_native_byte_order" in params


class TestNumpyPickler:
    """Test NumpyPickler class type hints."""

    def test_class_exists(self) -> None:
        """NumpyPickler should exist in runtime."""
        assert hasattr(mod, "NumpyPickler")
        assert inspect.isclass(mod.NumpyPickler)

    def test_inherits(self) -> None:
        """NumpyPickler should inherit from Pickler."""
        assert issubclass(mod.NumpyPickler, numpy_pickle_utils.Pickler)

    def test_init_signature(self) -> None:
        """NumpyPickler.__init__ should have correct signature."""
        sig = inspect.signature(mod.NumpyPickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "fp" in params
        assert "protocol" in params

    def test_save_method(self) -> None:
        """NumpyPickler.save should exist."""
        sig = inspect.signature(mod.NumpyPickler.save)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params


class TestNumpyUnpickler:
    """Test NumpyUnpickler class type hints."""

    def test_class_exists(self) -> None:
        """NumpyUnpickler should exist in runtime."""
        assert hasattr(mod, "NumpyUnpickler")
        assert inspect.isclass(mod.NumpyUnpickler)

    def test_inherits(self) -> None:
        """NumpyUnpickler should inherit from Unpickler."""
        assert issubclass(mod.NumpyUnpickler, numpy_pickle_utils.Unpickler)

    def test_init_signature(self) -> None:
        """NumpyUnpickler.__init__ should have correct signature."""
        sig = inspect.signature(mod.NumpyUnpickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "filename" in params
        assert "file_handle" in params
        assert "ensure_native_byte_order" in params
        assert "mmap_mode" in params

    def test_load_build_method(self) -> None:
        """NumpyUnpickler.load_build should exist."""
        sig = inspect.signature(mod.NumpyUnpickler.load_build)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestDump:
    """Test dump function type hints."""

    def test_exists(self) -> None:
        """dump should exist in runtime."""
        assert hasattr(mod, "dump")
        assert callable(mod.dump)

    def test_signature(self) -> None:
        """dump should have correct signature."""
        sig = inspect.signature(mod.dump)
        params = list(sig.parameters.keys())
        assert "value" in params
        assert "filename" in params
        assert "compress" in params
        assert "protocol" in params


class TestLoadTemporaryMemmap:
    """Test load_temporary_memmap function type hints."""

    def test_exists(self) -> None:
        """load_temporary_memmap should exist in runtime."""
        assert hasattr(mod, "load_temporary_memmap")
        assert callable(mod.load_temporary_memmap)

    def test_signature(self) -> None:
        """load_temporary_memmap should have correct signature."""
        sig = inspect.signature(mod.load_temporary_memmap)
        params = list(sig.parameters.keys())
        assert "filename" in params
        assert "mmap_mode" in params
        assert "unlink_on_gc_collect" in params


class TestLoad:
    """Test load function type hints."""

    def test_exists(self) -> None:
        """load should exist in runtime."""
        assert hasattr(mod, "load")
        assert callable(mod.load)

    def test_signature(self) -> None:
        """load should have correct signature."""
        sig = inspect.signature(mod.load)
        params = list(sig.parameters.keys())
        assert "filename" in params
        assert "mmap_mode" in params
        assert "ensure_native_byte_order" in params
