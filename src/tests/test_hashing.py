"""Tests for joblib.hashing stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.hashing as mod


class TestPickler:
    """Test Pickler type alias."""

    def test_exists(self) -> None:
        """Pickler should exist in runtime."""
        assert hasattr(mod, "Pickler")


class TestHasher:
    """Test Hasher class type hints."""

    def test_class_exists(self) -> None:
        """Hasher should exist in runtime."""
        assert hasattr(mod, "Hasher")
        assert inspect.isclass(mod.Hasher)

    def test_init_signature(self) -> None:
        """Hasher.__init__ should have correct signature."""
        sig = inspect.signature(mod.Hasher.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "hash_name" in params

    def test_attributes(self) -> None:
        """Hasher attributes should have correct types."""
        obj = mod.Hasher()
        assert hasattr(obj, "stream")

    def test_hash_method(self) -> None:
        """Hasher.hash should have correct signature."""
        sig = inspect.signature(mod.Hasher.hash)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params
        assert "return_digest" in params

    def test_hash_return_type(self) -> None:
        """Hasher.hash should return str."""
        hasher = mod.Hasher()
        result = hasher.hash("test")
        assert_type(result, str)
        assert isinstance(result, str)

    def test_save_method(self) -> None:
        """Hasher.save should exist."""
        sig = inspect.signature(mod.Hasher.save)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params

    def test_memoize_method(self) -> None:
        """Hasher.memoize should exist."""
        sig = inspect.signature(mod.Hasher.memoize)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params

    def test_save_global_method(self) -> None:
        """Hasher.save_global should exist."""
        sig = inspect.signature(mod.Hasher.save_global)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params
        assert "name" in params
        assert "pack" in params

    def test_save_set_method(self) -> None:
        """Hasher.save_set should exist."""
        sig = inspect.signature(mod.Hasher.save_set)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "set_items" in params


class TestNumpyHasher:
    """Test NumpyHasher class type hints."""

    def test_class_exists(self) -> None:
        """NumpyHasher should exist in runtime."""
        assert hasattr(mod, "NumpyHasher")
        assert inspect.isclass(mod.NumpyHasher)

    def test_inherits(self) -> None:
        """NumpyHasher should inherit from Hasher."""
        assert issubclass(mod.NumpyHasher, mod.Hasher)

    def test_init_signature(self) -> None:
        """NumpyHasher.__init__ should have correct signature."""
        sig = inspect.signature(mod.NumpyHasher.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "hash_name" in params
        assert "coerce_mmap" in params

    def test_attributes(self) -> None:
        """NumpyHasher attributes should have correct types."""
        obj = mod.NumpyHasher()
        assert_type(obj.coerce_mmap, bool)
        assert isinstance(obj.coerce_mmap, bool)
        assert hasattr(obj, "np")

    def test_save_method(self) -> None:
        """NumpyHasher.save should exist."""
        sig = inspect.signature(mod.NumpyHasher.save)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params


class TestHashFunction:
    """Test hash function type hints."""

    def test_exists(self) -> None:
        """hash function should exist in runtime."""
        assert hasattr(mod, "hash")
        assert callable(mod.hash)

    def test_signature(self) -> None:
        """hash should have correct signature."""
        sig = inspect.signature(mod.hash)
        params = list(sig.parameters.keys())
        assert "obj" in params
        assert "hash_name" in params
        assert "coerce_mmap" in params

    def test_return_type(self) -> None:
        """hash should return str."""
        result = mod.hash("test")
        assert_type(result, str)
        assert isinstance(result, str)
