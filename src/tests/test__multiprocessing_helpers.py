"""Tests for joblib._multiprocessing_helpers stub types."""

from __future__ import annotations

import multiprocessing
import types
from typing import assert_type

import joblib._multiprocessing_helpers as mod


class TestMp:
    """Test mp variable type hints."""

    def test_exists(self) -> None:
        """mp should exist in runtime."""
        assert hasattr(mod, "mp")

    def test_type(self) -> None:
        """mp should be ModuleType or None."""
        # stub check: mp is ModuleType | None
        assert_type(mod.mp, types.ModuleType | None)
        # runtime check
        assert mod.mp is None or isinstance(mod.mp, types.ModuleType)

    def test_is_multiprocessing_module(self) -> None:
        """mp should be multiprocessing module when available."""
        if mod.mp is not None:
            assert mod.mp is multiprocessing


class TestName:
    """Test name variable type hints."""

    def test_exists(self) -> None:
        """name should exist in runtime."""
        assert hasattr(mod, "name")

    def test_type(self) -> None:
        """name should be str."""
        assert_type(mod.name, str)
        assert isinstance(mod.name, str)


class TestAssertSpawning:
    """Test assert_spawning variable type hints."""

    def test_exists(self) -> None:
        """assert_spawning should exist in runtime."""
        assert hasattr(mod, "assert_spawning")

    def test_type(self) -> None:
        """assert_spawning should be callable or None."""
        assert mod.assert_spawning is None or callable(mod.assert_spawning)
