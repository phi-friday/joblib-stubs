"""Tests for joblib.parallel stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.parallel as parallel_runtime
from joblib._parallel_backends import SequentialBackend
from joblib.logger import Logger
from joblib.parallel import (
    BACKENDS,
    DEFAULT_BACKEND,
    DEFAULT_PROCESS_BACKEND,
    DEFAULT_THREAD_BACKEND,
    EXTERNAL_BACKENDS,
    MAYBE_AVAILABLE_BACKENDS,
    TASK_DONE,
    TASK_ERROR,
    TASK_PENDING,
    VALID_BACKEND_CONSTRAINTS,
    VALID_BACKEND_HINTS,
    BatchCompletionCallBack,
    BatchedCalls,
    Parallel,
    cpu_count,
    delayed,
    effective_n_jobs,
    get_active_backend,
    parallel_backend,
    parallel_config,
    register_parallel_backend,
)


class TestConstants:
    """Test module-level constants."""

    def test_backends_exists(self) -> None:
        """BACKENDS should exist in runtime."""
        assert hasattr(parallel_runtime, "BACKENDS")

    def test_backends_type(self) -> None:
        """BACKENDS should be a dict."""
        assert isinstance(BACKENDS, dict)

    def test_default_backend_exists(self) -> None:
        """DEFAULT_BACKEND should exist in runtime."""
        assert hasattr(parallel_runtime, "DEFAULT_BACKEND")

    def test_default_backend_type(self) -> None:
        """DEFAULT_BACKEND should be a str."""
        assert_type(DEFAULT_BACKEND, str)
        assert isinstance(DEFAULT_BACKEND, str)

    def test_default_thread_backend_exists(self) -> None:
        """DEFAULT_THREAD_BACKEND should exist in runtime."""
        assert hasattr(parallel_runtime, "DEFAULT_THREAD_BACKEND")

    def test_default_thread_backend_type(self) -> None:
        """DEFAULT_THREAD_BACKEND should be a str."""
        assert_type(DEFAULT_THREAD_BACKEND, str)
        assert isinstance(DEFAULT_THREAD_BACKEND, str)

    def test_default_process_backend_exists(self) -> None:
        """DEFAULT_PROCESS_BACKEND should exist in runtime."""
        assert hasattr(parallel_runtime, "DEFAULT_PROCESS_BACKEND")

    def test_default_process_backend_type(self) -> None:
        """DEFAULT_PROCESS_BACKEND should be a str."""
        assert_type(DEFAULT_PROCESS_BACKEND, str)
        assert isinstance(DEFAULT_PROCESS_BACKEND, str)

    def test_maybe_available_backends_exists(self) -> None:
        """MAYBE_AVAILABLE_BACKENDS should exist in runtime."""
        assert hasattr(parallel_runtime, "MAYBE_AVAILABLE_BACKENDS")

    def test_maybe_available_backends_type(self) -> None:
        """MAYBE_AVAILABLE_BACKENDS should be a set."""
        assert_type(MAYBE_AVAILABLE_BACKENDS, set[str])
        assert isinstance(MAYBE_AVAILABLE_BACKENDS, set)

    def test_external_backends_exists(self) -> None:
        """EXTERNAL_BACKENDS should exist in runtime."""
        assert hasattr(parallel_runtime, "EXTERNAL_BACKENDS")

    def test_external_backends_type(self) -> None:
        """EXTERNAL_BACKENDS should be a dict."""
        assert isinstance(EXTERNAL_BACKENDS, dict)

    def test_valid_backend_hints_exists(self) -> None:
        """VALID_BACKEND_HINTS should exist in runtime."""
        assert hasattr(parallel_runtime, "VALID_BACKEND_HINTS")

    def test_valid_backend_hints_type(self) -> None:
        """VALID_BACKEND_HINTS should be a tuple."""
        assert_type(VALID_BACKEND_HINTS, tuple[str | None, ...])
        assert isinstance(VALID_BACKEND_HINTS, tuple)

    def test_valid_backend_constraints_exists(self) -> None:
        """VALID_BACKEND_CONSTRAINTS should exist in runtime."""
        assert hasattr(parallel_runtime, "VALID_BACKEND_CONSTRAINTS")

    def test_valid_backend_constraints_type(self) -> None:
        """VALID_BACKEND_CONSTRAINTS should be a tuple."""
        assert_type(VALID_BACKEND_CONSTRAINTS, tuple[str | None, ...])
        assert isinstance(VALID_BACKEND_CONSTRAINTS, tuple)

    def test_task_done_exists(self) -> None:
        """TASK_DONE should exist in runtime."""
        assert hasattr(parallel_runtime, "TASK_DONE")

    def test_task_done_type(self) -> None:
        """TASK_DONE should be a str."""
        assert isinstance(TASK_DONE, str)

    def test_task_error_exists(self) -> None:
        """TASK_ERROR should exist in runtime."""
        assert hasattr(parallel_runtime, "TASK_ERROR")

    def test_task_error_type(self) -> None:
        """TASK_ERROR should be a str."""
        assert isinstance(TASK_ERROR, str)

    def test_task_pending_exists(self) -> None:
        """TASK_PENDING should exist in runtime."""
        assert hasattr(parallel_runtime, "TASK_PENDING")

    def test_task_pending_type(self) -> None:
        """TASK_PENDING should be a str."""
        assert isinstance(TASK_PENDING, str)


class TestGetActiveBackend:
    """Test get_active_backend function type hints."""

    def test_exists(self) -> None:
        """get_active_backend should exist in runtime."""
        assert hasattr(parallel_runtime, "get_active_backend")
        assert callable(parallel_runtime.get_active_backend)

    def test_signature(self) -> None:
        """get_active_backend should have correct signature."""
        sig = inspect.signature(get_active_backend)
        params = list(sig.parameters.keys())
        assert "prefer" in params
        assert "require" in params
        assert "verbose" in params

    def test_return_type(self) -> None:
        """get_active_backend should return tuple."""
        result = get_active_backend()
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestParallelConfig:
    """Test parallel_config class type hints."""

    def test_class_exists(self) -> None:
        """parallel_config should exist in runtime."""
        assert hasattr(parallel_runtime, "parallel_config")
        assert inspect.isclass(parallel_runtime.parallel_config)

    def test_init_signature(self) -> None:
        """parallel_config.__init__ should have correct signature."""
        sig = inspect.signature(parallel_config.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "backend" in params
        assert "n_jobs" in params
        assert "verbose" in params
        assert "temp_folder" in params
        assert "max_nbytes" in params
        assert "mmap_mode" in params
        assert "prefer" in params
        assert "require" in params
        assert "inner_max_num_threads" in params
        assert "backend_params" in params

    def test_enter_method(self) -> None:
        """parallel_config.__enter__ should exist."""
        sig = inspect.signature(parallel_config.__enter__)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_exit_method(self) -> None:
        """parallel_config.__exit__ should exist."""
        sig = inspect.signature(parallel_config.__exit__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "type" in params
        assert "value" in params
        assert "traceback" in params

    def test_unregister_method(self) -> None:
        """parallel_config.unregister should exist."""
        sig = inspect.signature(parallel_config.unregister)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestParallelBackend:
    """Test parallel_backend class type hints."""

    def test_class_exists(self) -> None:
        """parallel_backend should exist in runtime."""
        assert hasattr(parallel_runtime, "parallel_backend")
        assert inspect.isclass(parallel_runtime.parallel_backend)

    def test_inherits(self) -> None:
        """parallel_backend should inherit from parallel_config."""
        assert issubclass(parallel_backend, parallel_config)

    def test_init_signature(self) -> None:
        """parallel_backend.__init__ should have correct signature."""
        sig = inspect.signature(parallel_backend.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "backend" in params
        assert "n_jobs" in params
        assert "inner_max_num_threads" in params
        assert "backend_params" in params


class TestBatchedCalls:
    """Test BatchedCalls class type hints."""

    def test_class_exists(self) -> None:
        """BatchedCalls should exist in runtime."""
        assert hasattr(parallel_runtime, "BatchedCalls")
        assert inspect.isclass(parallel_runtime.BatchedCalls)

    def test_init_signature(self) -> None:
        """BatchedCalls.__init__ should have correct signature."""
        sig = inspect.signature(BatchedCalls.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "iterator_slice" in params
        assert "backend_and_jobs" in params
        assert "reducer_callback" in params
        assert "pickle_cache" in params

    def test_call_method(self) -> None:
        """BatchedCalls.__call__ should exist."""
        backend = SequentialBackend()
        obj = BatchedCalls([], backend)
        assert callable(obj)

    def test_reduce_method(self) -> None:
        """BatchedCalls.__reduce__ should exist."""
        backend = SequentialBackend()
        obj = BatchedCalls([], backend)
        assert hasattr(obj, "__reduce__")

    def test_len_method(self) -> None:
        """BatchedCalls.__len__ should exist."""
        backend = SequentialBackend()
        obj = BatchedCalls([], backend)
        assert hasattr(obj, "__len__")


class TestCpuCount:
    """Test cpu_count function type hints."""

    def test_exists(self) -> None:
        """cpu_count should exist in runtime."""
        assert hasattr(parallel_runtime, "cpu_count")
        assert callable(parallel_runtime.cpu_count)

    def test_signature(self) -> None:
        """cpu_count should have correct signature."""
        sig = inspect.signature(cpu_count)
        params = list(sig.parameters.keys())
        assert "only_physical_cores" in params

    def test_return_type(self) -> None:
        """cpu_count should return int."""
        result = cpu_count()
        assert_type(result, int)
        assert isinstance(result, int)


class TestDelayed:
    """Test delayed function type hints."""

    def test_exists(self) -> None:
        """delayed should exist in runtime."""
        assert hasattr(parallel_runtime, "delayed")
        assert callable(parallel_runtime.delayed)

    def test_signature(self) -> None:
        """delayed should have correct signature."""
        sig = inspect.signature(delayed)
        params = list(sig.parameters.keys())
        assert params == ["function"]

    def test_return_type(self) -> None:
        """delayed should return callable."""

        def sample_func(x: int) -> int:
            return x * 2

        result = delayed(sample_func)
        assert callable(result)


class TestBatchCompletionCallBack:
    """Test BatchCompletionCallBack class type hints."""

    def test_class_exists(self) -> None:
        """BatchCompletionCallBack should exist in runtime."""
        assert hasattr(parallel_runtime, "BatchCompletionCallBack")
        assert inspect.isclass(parallel_runtime.BatchCompletionCallBack)

    def test_init_signature(self) -> None:
        """BatchCompletionCallBack.__init__ should have correct signature."""
        sig = inspect.signature(BatchCompletionCallBack.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "dispatch_timestamp" in params
        assert "batch_size" in params
        assert "parallel" in params

    def test_register_job_method(self) -> None:
        """BatchCompletionCallBack.register_job should exist."""
        sig = inspect.signature(BatchCompletionCallBack.register_job)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "job" in params

    def test_get_result_method(self) -> None:
        """BatchCompletionCallBack.get_result should exist."""
        sig = inspect.signature(BatchCompletionCallBack.get_result)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "timeout" in params

    def test_get_status_method(self) -> None:
        """BatchCompletionCallBack.get_status should exist."""
        sig = inspect.signature(BatchCompletionCallBack.get_status)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "timeout" in params


class TestRegisterParallelBackend:
    """Test register_parallel_backend function type hints."""

    def test_exists(self) -> None:
        """register_parallel_backend should exist in runtime."""
        assert hasattr(parallel_runtime, "register_parallel_backend")
        assert callable(parallel_runtime.register_parallel_backend)

    def test_signature(self) -> None:
        """register_parallel_backend should have correct signature."""
        sig = inspect.signature(register_parallel_backend)
        params = list(sig.parameters.keys())
        assert "name" in params
        assert "factory" in params
        assert "make_default" in params


class TestEffectiveNJobs:
    """Test effective_n_jobs function type hints."""

    def test_exists(self) -> None:
        """effective_n_jobs should exist in runtime."""
        assert hasattr(parallel_runtime, "effective_n_jobs")
        assert callable(parallel_runtime.effective_n_jobs)

    def test_signature(self) -> None:
        """effective_n_jobs should have correct signature."""
        sig = inspect.signature(effective_n_jobs)
        params = list(sig.parameters.keys())
        assert "n_jobs" in params

    def test_return_type(self) -> None:
        """effective_n_jobs should return int."""
        result = effective_n_jobs()
        assert_type(result, int)
        assert isinstance(result, int)


class TestParallel:
    """Test Parallel class type hints."""

    def test_class_exists(self) -> None:
        """Parallel should exist in runtime."""
        assert hasattr(parallel_runtime, "Parallel")
        assert inspect.isclass(parallel_runtime.Parallel)

    def test_inherits(self) -> None:
        """Parallel should inherit from Logger."""
        assert issubclass(Parallel, Logger)

    def test_init_signature(self) -> None:
        """Parallel.__init__ should have correct signature."""
        sig = inspect.signature(Parallel.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "n_jobs" in params
        assert "backend" in params
        assert "return_as" in params
        assert "verbose" in params
        assert "timeout" in params
        assert "pre_dispatch" in params
        assert "batch_size" in params
        assert "temp_folder" in params
        assert "max_nbytes" in params
        assert "mmap_mode" in params
        assert "prefer" in params
        assert "require" in params
        assert "backend_kwargs" in params

    def test_call_method(self) -> None:
        """Parallel.__call__ should exist."""
        parallel = Parallel(n_jobs=1)
        assert callable(parallel)

    def test_parallel_instantiation(self) -> None:
        """Parallel should be instantiable."""
        parallel = Parallel(n_jobs=1)
        assert_type(parallel.n_jobs, int)
        assert isinstance(parallel.n_jobs, int)
