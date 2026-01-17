"""Tests for joblib.numpy_pickle_utils stub types."""

from __future__ import annotations

from typing import assert_type

import joblib.numpy_pickle_utils as mod


class TestPickler:
    """Test Pickler type alias."""

    def test_exists(self) -> None:
        """Pickler should exist in runtime."""
        assert hasattr(mod, "Pickler")


class TestUnpickler:
    """Test Unpickler type alias."""

    def test_exists(self) -> None:
        """Unpickler should exist in runtime."""
        assert hasattr(mod, "Unpickler")


class TestXrange:
    """Test xrange type alias."""

    def test_exists(self) -> None:
        """xrange should exist in runtime."""
        assert hasattr(mod, "xrange")

    def test_xrange_is_range(self) -> None:
        """xrange should be range in Python 3."""
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
