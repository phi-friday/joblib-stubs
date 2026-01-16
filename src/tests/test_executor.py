"""Tests for joblib.executor stub types."""

from __future__ import annotations

import inspect
from concurrent import futures
from typing import assert_type

import joblib.executor as executor_runtime
from joblib.executor import MemmappingExecutor, get_memmapping_executor
from joblib.externals.loky.reusable_executor import _ReusablePoolExecutor


class TestGetMemmappingExecutor:
    """Test get_memmapping_executor type hints."""

    def test_exists(self) -> None:
        """get_memmapping_executor should exist in runtime."""
        assert hasattr(executor_runtime, "get_memmapping_executor")
        assert callable(executor_runtime.get_memmapping_executor)

    def test_signature(self) -> None:
        """get_memmapping_executor should have correct signature."""
        sig = inspect.signature(get_memmapping_executor)
        params = list(sig.parameters.keys())
        assert "n_jobs" in params
        assert "kwargs" in params

    def test_return_type(self) -> None:
        """get_memmapping_executor should return Executor."""
        result = get_memmapping_executor(1)
        assert_type(result, futures.Executor)
        assert isinstance(result, futures.Executor)


class TestMemmappingExecutor:
    """Test MemmappingExecutor type hints."""

    def test_class_exists(self) -> None:
        """MemmappingExecutor should exist in runtime."""
        assert hasattr(executor_runtime, "MemmappingExecutor")
        assert inspect.isclass(executor_runtime.MemmappingExecutor)

    def test_inherits(self) -> None:
        """MemmappingExecutor should inherit from _ReusablePoolExecutor."""
        assert issubclass(MemmappingExecutor, _ReusablePoolExecutor)

    def test_init_signature(self) -> None:
        """MemmappingExecutor.__init__ should have correct signature."""
        sig = inspect.signature(MemmappingExecutor.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "submit_resize_lock" in params
        assert "max_workers" in params
        assert "context" in params
        assert "timeout" in params
        assert "executor_id" in params
        assert "job_reducers" in params
        assert "result_reducers" in params
        assert "initializer" in params
        assert "initargs" in params
        assert "env" in params

    def test_get_memmapping_executor_exists(self) -> None:
        """MemmappingExecutor.get_memmapping_executor should exist in runtime."""
        assert hasattr(MemmappingExecutor, "get_memmapping_executor")
        assert callable(MemmappingExecutor.get_memmapping_executor)

    def test_get_memmapping_executor_signature(self) -> None:
        """MemmappingExecutor.get_memmapping_executor should have correct signature."""
        sig = inspect.signature(MemmappingExecutor.get_memmapping_executor)
        params = list(sig.parameters.keys())
        assert "n_jobs" in params
        assert "timeout" in params
        assert "initializer" in params
        assert "initargs" in params
        assert "env" in params
        assert "temp_folder" in params
        assert "context_id" in params
        assert "backend_args" in params

    def test_get_memmapping_executor_return_type(self) -> None:
        """MemmappingExecutor.get_memmapping_executor should return Executor."""
        result = MemmappingExecutor.get_memmapping_executor(1)
        assert_type(result, futures.Executor)
        assert isinstance(result, futures.Executor)

    def test_terminate_exists(self) -> None:
        """MemmappingExecutor.terminate should exist in runtime."""
        assert hasattr(MemmappingExecutor, "terminate")
        assert callable(MemmappingExecutor.terminate)

    def test_terminate_signature(self) -> None:
        """MemmappingExecutor.terminate should have correct signature."""
        sig = inspect.signature(MemmappingExecutor.terminate)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "kill_workers" in params
