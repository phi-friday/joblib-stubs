"""Tests for joblib.numpy_pickle_utils stub types."""

from __future__ import annotations

import pickle
from typing import assert_type

import joblib.numpy_pickle_utils as mod


class TestPickler:
    """Test Pickler type alias."""

    def test_exists(self) -> None:
        """Pickler should exist in runtime."""
        assert hasattr(mod, "Pickler")

    def test_type(self) -> None:
        """Pickler should be pickle._Pickler."""
        assert_type(mod.Pickler, type[pickle._Pickler])  # noqa: SLF001
        assert mod.Pickler is pickle._Pickler  # noqa: SLF001


class TestUnpickler:
    """Test Unpickler type alias."""

    def test_exists(self) -> None:
        """Unpickler should exist in runtime."""
        assert hasattr(mod, "Unpickler")

    def test_type(self) -> None:
        """Unpickler should be pickle._Unpickler."""
        assert_type(mod.Unpickler, type[pickle._Unpickler])  # noqa: SLF001
        assert mod.Unpickler is pickle._Unpickler  # noqa: SLF001


class TestXrange:
    """Test xrange type alias."""

    def test_exists(self) -> None:
        """xrange should exist in runtime."""
        assert hasattr(mod, "xrange")

    def test_type(self) -> None:
        """xrange should be range."""
        assert_type(mod.xrange, type[range])
        assert mod.xrange is range


class TestBufferSize:
    """Test BUFFER_SIZE constant."""

    def test_exists(self) -> None:
        """BUFFER_SIZE should exist in runtime."""
        assert hasattr(mod, "BUFFER_SIZE")

    def test_type(self) -> None:
        """BUFFER_SIZE should be an int."""
        assert_type(mod.BUFFER_SIZE, int)
        assert isinstance(mod.BUFFER_SIZE, int)
