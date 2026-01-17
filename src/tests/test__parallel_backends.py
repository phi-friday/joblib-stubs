"""Tests for joblib._parallel_backends stub types."""

from __future__ import annotations

import inspect
from abc import ABCMeta

import joblib._parallel_backends as mod


class TestParallelBackendBase:
    """Test ParallelBackendBase class."""

    def test_exists(self) -> None:
        """ParallelBackendBase should exist."""
        assert hasattr(mod, "ParallelBackendBase")

    def test_is_class(self) -> None:
        """ParallelBackendBase should be a class."""
        assert inspect.isclass(mod.ParallelBackendBase)

    def test_is_abstract(self) -> None:
        """ParallelBackendBase should be abstract."""
        assert isinstance(mod.ParallelBackendBase, ABCMeta)

    def test_class_vars_exist(self) -> None:
        """ParallelBackendBase should have class variables."""
        assert hasattr(mod.ParallelBackendBase, "default_n_jobs")
        assert hasattr(mod.ParallelBackendBase, "supports_inner_max_num_threads")
        assert hasattr(mod.ParallelBackendBase, "supports_retrieve_callback")

    def test_methods_exist(self) -> None:
        """ParallelBackendBase should have required methods."""
        assert hasattr(mod.ParallelBackendBase, "effective_n_jobs")
        assert hasattr(mod.ParallelBackendBase, "configure")
        assert hasattr(mod.ParallelBackendBase, "terminate")
        assert hasattr(mod.ParallelBackendBase, "abort_everything")
        assert hasattr(mod.ParallelBackendBase, "get_nested_backend")


class TestSequentialBackend:
    """Test SequentialBackend class."""

    def test_exists(self) -> None:
        """SequentialBackend should exist."""
        assert hasattr(mod, "SequentialBackend")

    def test_is_class(self) -> None:
        """SequentialBackend should be a class."""
        assert inspect.isclass(mod.SequentialBackend)

    def test_inherits(self) -> None:
        """SequentialBackend should inherit from ParallelBackendBase."""
        assert issubclass(mod.SequentialBackend, mod.ParallelBackendBase)


class TestPoolManagerMixin:
    """Test PoolManagerMixin class."""

    def test_exists(self) -> None:
        """PoolManagerMixin should exist."""
        assert hasattr(mod, "PoolManagerMixin")

    def test_is_class(self) -> None:
        """PoolManagerMixin should be a class."""
        assert inspect.isclass(mod.PoolManagerMixin)

    def test_methods_exist(self) -> None:
        """PoolManagerMixin should have required methods."""
        assert hasattr(mod.PoolManagerMixin, "effective_n_jobs")
        assert hasattr(mod.PoolManagerMixin, "terminate")
        assert hasattr(mod.PoolManagerMixin, "submit")


class TestAutoBatchingMixin:
    """Test AutoBatchingMixin class."""

    def test_exists(self) -> None:
        """AutoBatchingMixin should exist."""
        assert hasattr(mod, "AutoBatchingMixin")

    def test_is_class(self) -> None:
        """AutoBatchingMixin should be a class."""
        assert inspect.isclass(mod.AutoBatchingMixin)

    def test_class_vars_exist(self) -> None:
        """AutoBatchingMixin should have class variables."""
        assert hasattr(mod.AutoBatchingMixin, "MIN_IDEAL_BATCH_DURATION")
        assert hasattr(mod.AutoBatchingMixin, "MAX_IDEAL_BATCH_DURATION")

    def test_methods_exist(self) -> None:
        """AutoBatchingMixin should have required methods."""
        assert hasattr(mod.AutoBatchingMixin, "compute_batch_size")
        assert hasattr(mod.AutoBatchingMixin, "batch_completed")
        assert hasattr(mod.AutoBatchingMixin, "reset_batch_stats")


class TestThreadingBackend:
    """Test ThreadingBackend class."""

    def test_exists(self) -> None:
        """ThreadingBackend should exist."""
        assert hasattr(mod, "ThreadingBackend")

    def test_is_class(self) -> None:
        """ThreadingBackend should be a class."""
        assert inspect.isclass(mod.ThreadingBackend)

    def test_inherits(self) -> None:
        """ThreadingBackend should inherit from correct bases."""
        assert issubclass(mod.ThreadingBackend, mod.PoolManagerMixin)
        assert issubclass(mod.ThreadingBackend, mod.ParallelBackendBase)


class TestMultiprocessingBackend:
    """Test MultiprocessingBackend class."""

    def test_exists(self) -> None:
        """MultiprocessingBackend should exist."""
        assert hasattr(mod, "MultiprocessingBackend")

    def test_is_class(self) -> None:
        """MultiprocessingBackend should be a class."""
        assert inspect.isclass(mod.MultiprocessingBackend)

    def test_inherits(self) -> None:
        """MultiprocessingBackend should inherit from correct bases."""
        assert issubclass(mod.MultiprocessingBackend, mod.PoolManagerMixin)
        assert issubclass(mod.MultiprocessingBackend, mod.AutoBatchingMixin)
        assert issubclass(mod.MultiprocessingBackend, mod.ParallelBackendBase)


class TestLokyBackend:
    """Test LokyBackend class."""

    def test_exists(self) -> None:
        """LokyBackend should exist."""
        assert hasattr(mod, "LokyBackend")

    def test_is_class(self) -> None:
        """LokyBackend should be a class."""
        assert inspect.isclass(mod.LokyBackend)

    def test_inherits(self) -> None:
        """LokyBackend should inherit from correct bases."""
        assert issubclass(mod.LokyBackend, mod.AutoBatchingMixin)
        assert issubclass(mod.LokyBackend, mod.ParallelBackendBase)


class TestFallbackToBackend:
    """Test FallbackToBackend exception."""

    def test_exists(self) -> None:
        """FallbackToBackend should exist."""
        assert hasattr(mod, "FallbackToBackend")

    def test_is_class(self) -> None:
        """FallbackToBackend should be a class."""
        assert inspect.isclass(mod.FallbackToBackend)

    def test_is_exception(self) -> None:
        """FallbackToBackend should be an exception."""
        assert issubclass(mod.FallbackToBackend, Exception)

    def test_init_signature(self) -> None:
        """FallbackToBackend.__init__ should have correct signature."""
        sig = inspect.signature(mod.FallbackToBackend.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "backend" in params


class TestInsideDaskWorker:
    """Test inside_dask_worker function."""

    def test_exists(self) -> None:
        """inside_dask_worker should exist."""
        assert hasattr(mod, "inside_dask_worker")

    def test_callable(self) -> None:
        """inside_dask_worker should be callable."""
        assert callable(mod.inside_dask_worker)

    def test_returns_bool(self) -> None:
        """inside_dask_worker should return bool."""
        result = mod.inside_dask_worker()
        assert isinstance(result, bool)
