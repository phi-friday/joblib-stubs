"""Tests for joblib.backports stub types."""

from __future__ import annotations

import inspect
import re
from pathlib import Path
from typing import Any, Literal, assert_type

import joblib.backports as backports_runtime
import numpy as np
from joblib.backports import LooseVersion, Version, concurrency_safe_rename, make_memmap


class TestVersion:
    """Test Version class type hints."""

    def test_version_class_exists(self) -> None:
        """Version class should exist in runtime."""
        assert hasattr(backports_runtime, "Version")
        assert inspect.isclass(backports_runtime.Version)

    def test_version_init_signature(self) -> None:
        """Version.__init__ should accept optional str parameter."""
        sig = inspect.signature(Version.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "vstring" in params

    def test_version_comparison_methods(self) -> None:
        """Version should have comparison methods."""
        # Version is an abstract base class without parse() method
        # Use LooseVersion instead
        v1 = LooseVersion("1.0")
        v2 = LooseVersion("2.0")

        # Test comparison operators return bool
        assert_type(v1 == v2, bool)
        assert_type(v1 != v2, bool)
        assert_type(v1 < v2, bool)
        assert_type(v1 <= v2, bool)
        assert_type(v1 > v2, bool)
        assert_type(v1 >= v2, bool)

    def test_version_returns_bool(self) -> None:
        """Version comparison methods should return bool."""
        v1 = LooseVersion("1.0")
        v2 = LooseVersion("2.0")

        # Runtime verification
        assert isinstance(v1 == v2, bool)
        assert isinstance(v1 < v2, bool)
        assert isinstance(v1 <= v2, bool)
        assert isinstance(v1 > v2, bool)
        assert isinstance(v1 >= v2, bool)


class TestLooseVersion:
    """Test LooseVersion class type hints."""

    def test_looseversion_class_exists(self) -> None:
        """LooseVersion class should exist in runtime."""
        assert hasattr(backports_runtime, "LooseVersion")
        assert inspect.isclass(backports_runtime.LooseVersion)

    def test_looseversion_inherits_version(self) -> None:
        """LooseVersion should inherit from Version."""
        assert issubclass(LooseVersion, Version)

    def test_looseversion_has_component_re(self) -> None:
        """LooseVersion should have component_re attribute."""
        assert hasattr(LooseVersion, "component_re")
        # Type check: component_re should be Pattern[str]
        assert_type(LooseVersion.component_re, re.Pattern[str])
        # Runtime check
        assert isinstance(LooseVersion.component_re, re.Pattern)

    def test_looseversion_attributes(self) -> None:
        """LooseVersion instance should have vstring and version attributes."""
        lv = LooseVersion("1.2.3")
        assert hasattr(lv, "vstring")
        assert hasattr(lv, "version")

        # Type checks
        assert_type(lv.vstring, str)
        assert_type(lv.version, list[str | int])

        # Runtime checks
        assert isinstance(lv.vstring, str)
        assert isinstance(lv.version, list)

    def test_looseversion_parse_signature(self) -> None:
        """LooseVersion.parse should accept str parameter."""
        sig = inspect.signature(LooseVersion.parse)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "vstring" in params

    def test_looseversion_parse_returns_none(self) -> None:
        """LooseVersion.parse should return None."""
        lv = LooseVersion("1.0")
        # Type check: parse returns None
        assert_type(lv.parse("2.0"), None)
        # Verify parse modified the object in place
        assert lv.vstring == "2.0"


class TestMakeMemmap:
    """Test make_memmap function type hints."""

    def test_make_memmap_exists(self) -> None:
        """make_memmap function should exist in runtime."""
        assert hasattr(backports_runtime, "make_memmap")
        assert callable(backports_runtime.make_memmap)

    def test_make_memmap_signature(self) -> None:
        """make_memmap should have correct parameters."""
        sig = inspect.signature(make_memmap)
        params = list(sig.parameters.keys())

        expected_params = [
            "filename",
            "dtype",
            "mode",
            "offset",
            "shape",
            "order",
            "unlink_on_gc_collect",
        ]
        for param in expected_params:
            assert param in params, f"Parameter '{param}' missing"

    def test_make_memmap_returns_memmap(self, tmp_path: Path) -> None:
        """make_memmap should return numpy memmap."""
        filename = tmp_path / "test.mmap"
        result = make_memmap(filename, dtype=np.float32, shape=(10, 10), mode="w+")

        # Type check
        assert_type(result, np.memmap[Any, np.dtype[Any]])
        # Runtime check
        assert isinstance(result, np.memmap)

    def test_make_memmap_accepts_str_path(self, tmp_path: Path) -> None:
        """make_memmap should accept str path (StrOrBytesPath)."""
        filename = str(tmp_path / "test.mmap")
        result = make_memmap(filename, dtype=np.float32, shape=(10,), mode="w+")
        # Type check
        assert_type(result, np.memmap[Any, np.dtype[Any]])
        # Runtime check
        assert isinstance(result, np.memmap)

    def test_make_memmap_accepts_bytes_path(self, tmp_path: Path) -> None:
        """make_memmap should accept bytes path (StrOrBytesPath)."""
        filename = bytes(tmp_path / "test.mmap")
        result = make_memmap(filename, dtype=np.float32, shape=(10,), mode="w+")
        # Type check
        assert_type(result, np.memmap[Any, np.dtype[Any]])
        # Runtime check
        assert isinstance(result, np.memmap)

    def test_make_memmap_mode_parameter(self, tmp_path: Path) -> None:
        """make_memmap mode should accept MmapMode values."""
        # MmapMode should accept these values
        modes: list[Literal["r", "r+", "w+", "c"]] = ["r", "r+", "w+", "c"]
        for mode in modes:
            f = tmp_path / f"test_{mode}.mmap"
            # Create file first for all modes except 'w+'
            if mode != "w+":
                make_memmap(f, dtype=np.float32, shape=(5,), mode="w+")
            result = make_memmap(f, dtype=np.float32, shape=(5,), mode=mode)
            # Type check
            assert_type(result, np.memmap[Any, np.dtype[Any]])
            # Runtime check
            assert isinstance(result, np.memmap)

    def test_make_memmap_order_parameter(self, tmp_path: Path) -> None:
        """make_memmap order should accept Literal values."""
        # Test valid order values
        orders: list[Literal["K", "A", "C", "F"]] = ["K", "A", "C", "F"]
        for order in orders:
            f = tmp_path / f"test_{order}.mmap"
            result = make_memmap(
                f, dtype=np.float32, shape=(5,), mode="w+", order=order
            )
            # Type check
            assert_type(result, np.memmap[Any, np.dtype[Any]])
            # Runtime check
            assert isinstance(result, np.memmap)


class TestConcurrencySafeRename:
    """Test concurrency_safe_rename function type hints."""

    def test_concurrency_safe_rename_exists(self) -> None:
        """concurrency_safe_rename function should exist in runtime."""
        assert hasattr(backports_runtime, "concurrency_safe_rename")
        assert callable(backports_runtime.concurrency_safe_rename)

    def test_concurrency_safe_rename_signature(self) -> None:
        """concurrency_safe_rename should have correct parameters."""
        sig = inspect.signature(concurrency_safe_rename)
        params = list(sig.parameters.keys())

        assert "src" in params
        assert "dst" in params

    def test_concurrency_safe_rename_returns_none(self, tmp_path: Path) -> None:
        """concurrency_safe_rename should return None."""
        src = tmp_path / "source.txt"
        dst = tmp_path / "dest.txt"
        src.write_text("test")

        # Type check: function returns None
        assert_type(concurrency_safe_rename(src, dst), None)
        # Function performs the rename
        assert dst.exists()
        assert not src.exists()

    def test_concurrency_safe_rename_accepts_str(self, tmp_path: Path) -> None:
        """concurrency_safe_rename should accept str paths."""
        src = tmp_path / "source2.txt"
        dst = tmp_path / "dest2.txt"
        src.write_text("test")

        # Type check: function returns None
        assert_type(concurrency_safe_rename(str(src), str(dst)), None)
        assert dst.exists()

    def test_concurrency_safe_rename_accepts_bytes(self, tmp_path: Path) -> None:
        """concurrency_safe_rename should accept bytes paths."""
        src = tmp_path / "source3.txt"
        dst = tmp_path / "dest3.txt"
        src.write_text("test")

        # Type check: function returns None
        assert_type(concurrency_safe_rename(bytes(src), bytes(dst)), None)
        assert dst.exists()
