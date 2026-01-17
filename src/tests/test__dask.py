"""Tests for joblib._dask stub types."""

from __future__ import annotations

import inspect

import joblib._dask as mod
from joblib._parallel_backends import AutoBatchingMixin, ParallelBackendBase


class TestIsWeakrefable:
    """Test is_weakrefable function."""

    def test_exists(self) -> None:
        """is_weakrefable should exist."""
        assert hasattr(mod, "is_weakrefable")

    def test_callable(self) -> None:
        """is_weakrefable should be callable."""
        assert callable(mod.is_weakrefable)

    def test_signature(self) -> None:
        """is_weakrefable should have correct signature."""
        sig = inspect.signature(mod.is_weakrefable)
        params = list(sig.parameters.keys())
        assert "obj" in params

    def test_returns_bool(self) -> None:
        """is_weakrefable should return bool."""
        result = mod.is_weakrefable(object())
        assert isinstance(result, bool)


class TestBatch:
    """Test Batch class."""

    def test_exists(self) -> None:
        """Batch should exist."""
        assert hasattr(mod, "Batch")

    def test_is_class(self) -> None:
        """Batch should be a class."""
        assert inspect.isclass(mod.Batch)

    def test_is_callable(self) -> None:
        """Batch instances should be callable."""
        assert callable(mod.Batch)


class TestDaskDistributedBackend:
    """Test DaskDistributedBackend class."""

    def test_exists(self) -> None:
        """DaskDistributedBackend should exist."""
        assert hasattr(mod, "DaskDistributedBackend")

    def test_is_class(self) -> None:
        """DaskDistributedBackend should be a class."""
        assert inspect.isclass(mod.DaskDistributedBackend)

    def test_inherits_auto_batching_mixin(self) -> None:
        """DaskDistributedBackend should inherit from AutoBatchingMixin."""
        assert issubclass(mod.DaskDistributedBackend, AutoBatchingMixin)

    def test_inherits_parallel_backend_base(self) -> None:
        """DaskDistributedBackend should inherit from ParallelBackendBase."""
        assert issubclass(mod.DaskDistributedBackend, ParallelBackendBase)

    def test_init_signature(self) -> None:
        """DaskDistributedBackend.__init__ should have correct signature."""
        sig = inspect.signature(mod.DaskDistributedBackend.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "scheduler_host" in params
        assert "scatter" in params
        assert "client" in params
        assert "loop" in params
        assert "wait_for_workers_timeout" in params

    def test_methods_exist(self) -> None:
        """DaskDistributedBackend should have required methods."""
        assert hasattr(mod.DaskDistributedBackend, "__reduce__")
        assert hasattr(mod.DaskDistributedBackend, "get_nested_backend")
        assert hasattr(mod.DaskDistributedBackend, "configure")
        assert hasattr(mod.DaskDistributedBackend, "apply_async")
        assert hasattr(mod.DaskDistributedBackend, "effective_n_jobs")
