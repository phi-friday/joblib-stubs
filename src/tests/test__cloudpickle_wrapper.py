"""Tests for joblib._cloudpickle_wrapper stub types."""

from __future__ import annotations

import inspect

import joblib._cloudpickle_wrapper as mod


class TestWrapNonPicklableObjects:
    """Test wrap_non_picklable_objects function type hints."""

    def test_exists(self) -> None:
        """wrap_non_picklable_objects should exist in runtime."""
        assert hasattr(mod, "wrap_non_picklable_objects")

    def test_callable(self) -> None:
        """wrap_non_picklable_objects should be callable."""
        assert callable(mod.wrap_non_picklable_objects)

    def test_signature(self) -> None:
        """wrap_non_picklable_objects should have correct signature."""
        sig = inspect.signature(mod.wrap_non_picklable_objects)
        params = list(sig.parameters.keys())
        assert "obj" in params
        assert "keep_wrapper" in params


class TestModuleAll:
    """Test module __all__ attribute."""

    def test_all_exists(self) -> None:
        """__all__ should exist."""
        assert hasattr(mod, "__all__")

    def test_all_contents(self) -> None:
        """__all__ should contain wrap_non_picklable_objects."""
        assert "wrap_non_picklable_objects" in mod.__all__
