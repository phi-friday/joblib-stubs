"""Tests for joblib._store_backends stub types."""

from __future__ import annotations

import inspect
from abc import ABCMeta
from datetime import datetime

import joblib._store_backends as mod


class TestCacheItemInfo:
    """Test CacheItemInfo named tuple."""

    def test_exists(self) -> None:
        """CacheItemInfo should exist."""
        assert hasattr(mod, "CacheItemInfo")

    def test_is_namedtuple(self) -> None:
        """CacheItemInfo should be a namedtuple."""
        assert hasattr(mod.CacheItemInfo, "_fields")
        assert issubclass(mod.CacheItemInfo, tuple)

    def test_fields(self) -> None:
        """CacheItemInfo should have correct fields."""
        assert mod.CacheItemInfo._fields == ("path", "size", "last_access")

    def test_field_types(self) -> None:
        """CacheItemInfo fields should have correct types."""
        info = mod.CacheItemInfo(
            path="test_path",
            size=100,
            last_access=datetime.now(tz=None),  # noqa: DTZ005
        )
        assert isinstance(info.path, str)
        assert isinstance(info.size, int)
        assert isinstance(info.last_access, datetime)


class TestCacheWarning:
    """Test CacheWarning class."""

    def test_exists(self) -> None:
        """CacheWarning should exist."""
        assert hasattr(mod, "CacheWarning")

    def test_is_class(self) -> None:
        """CacheWarning should be a class."""
        assert inspect.isclass(mod.CacheWarning)

    def test_is_warning(self) -> None:
        """CacheWarning should inherit from Warning."""
        assert issubclass(mod.CacheWarning, Warning)


class TestConcurrencySafeWrite:
    """Test concurrency_safe_write function."""

    def test_exists(self) -> None:
        """concurrency_safe_write should exist."""
        assert hasattr(mod, "concurrency_safe_write")

    def test_callable(self) -> None:
        """concurrency_safe_write should be callable."""
        assert callable(mod.concurrency_safe_write)

    def test_signature(self) -> None:
        """concurrency_safe_write should have correct signature."""
        sig = inspect.signature(mod.concurrency_safe_write)
        params = list(sig.parameters.keys())
        assert "object_to_write" in params
        assert "filename" in params
        assert "write_func" in params


class TestStoreBackendBase:
    """Test StoreBackendBase class."""

    def test_exists(self) -> None:
        """StoreBackendBase should exist."""
        assert hasattr(mod, "StoreBackendBase")

    def test_is_class(self) -> None:
        """StoreBackendBase should be a class."""
        assert inspect.isclass(mod.StoreBackendBase)

    def test_is_abstract(self) -> None:
        """StoreBackendBase should be abstract."""
        assert isinstance(mod.StoreBackendBase, ABCMeta)

    def test_abstract_methods_exist(self) -> None:
        """StoreBackendBase should have abstract methods."""
        assert hasattr(mod.StoreBackendBase, "create_location")
        assert hasattr(mod.StoreBackendBase, "clear_location")
        assert hasattr(mod.StoreBackendBase, "get_items")
        assert hasattr(mod.StoreBackendBase, "configure")


class TestStoreBackendMixin:
    """Test StoreBackendMixin class."""

    def test_exists(self) -> None:
        """StoreBackendMixin should exist."""
        assert hasattr(mod, "StoreBackendMixin")

    def test_is_class(self) -> None:
        """StoreBackendMixin should be a class."""
        assert inspect.isclass(mod.StoreBackendMixin)

    def test_methods_exist(self) -> None:
        """StoreBackendMixin should have required methods."""
        methods = [
            "load_item",
            "dump_item",
            "clear_item",
            "contains_item",
            "get_item_info",
            "get_metadata",
            "store_metadata",
            "contains_path",
            "clear_path",
            "store_cached_func_code",
            "get_cached_func_code",
            "get_cached_func_info",
            "clear",
            "enforce_store_limits",
        ]
        for method in methods:
            assert hasattr(mod.StoreBackendMixin, method), f"Missing method: {method}"


class TestFileSystemStoreBackend:
    """Test FileSystemStoreBackend class."""

    def test_exists(self) -> None:
        """FileSystemStoreBackend should exist."""
        assert hasattr(mod, "FileSystemStoreBackend")

    def test_is_class(self) -> None:
        """FileSystemStoreBackend should be a class."""
        assert inspect.isclass(mod.FileSystemStoreBackend)

    def test_inherits(self) -> None:
        """FileSystemStoreBackend should inherit from correct bases."""
        assert issubclass(mod.FileSystemStoreBackend, mod.StoreBackendBase)
        assert issubclass(mod.FileSystemStoreBackend, mod.StoreBackendMixin)
