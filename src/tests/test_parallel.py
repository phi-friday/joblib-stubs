"""Tests for joblib.parallel stub types."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Literal, assert_type

import joblib.parallel as mod


class TestModuleConstants:
    """Test module-level constants and variables."""

    def test_backends_exists(self) -> None:
        """BACKENDS should exist in runtime."""
        assert hasattr(mod, "BACKENDS")

    def test_backends_type(self) -> None:
        """BACKENDS should be a dict."""
        if TYPE_CHECKING:
            assert_type(mod.BACKENDS, dict[str, type[mod.ParallelBackendBase[Any]]])
        assert isinstance(mod.BACKENDS, dict)

    def test_default_backend_exists(self) -> None:
        """DEFAULT_BACKEND should exist in runtime."""
        assert hasattr(mod, "DEFAULT_BACKEND")

    def test_default_backend_type(self) -> None:
        """DEFAULT_BACKEND should be a str."""
        assert_type(mod.DEFAULT_BACKEND, str)
        assert isinstance(mod.DEFAULT_BACKEND, str)

    def test_default_thread_backend_exists(self) -> None:
        """DEFAULT_THREAD_BACKEND should exist in runtime."""
        assert hasattr(mod, "DEFAULT_THREAD_BACKEND")
        assert isinstance(mod.DEFAULT_THREAD_BACKEND, str)

    def test_default_process_backend_exists(self) -> None:
        """DEFAULT_PROCESS_BACKEND should exist in runtime."""
        assert hasattr(mod, "DEFAULT_PROCESS_BACKEND")
        assert isinstance(mod.DEFAULT_PROCESS_BACKEND, str)

    def test_task_literals_exist(self) -> None:
        """TASK_DONE, TASK_ERROR, TASK_PENDING should exist."""
        assert hasattr(mod, "TASK_DONE")
        assert hasattr(mod, "TASK_ERROR")
        assert hasattr(mod, "TASK_PENDING")


class TestGetActiveBackend:
    """Test get_active_backend function type hints."""

    def test_exists(self) -> None:
        """get_active_backend should exist in runtime."""
        assert hasattr(mod, "get_active_backend")
        assert callable(mod.get_active_backend)

    def test_signature(self) -> None:
        """get_active_backend should have correct signature."""
        sig = inspect.signature(mod.get_active_backend)
        params = list(sig.parameters.keys())
        assert "prefer" in params
        assert "require" in params
        assert "verbose" in params

    def test_return_type(self) -> None:
        """get_active_backend should return tuple."""
        result = mod.get_active_backend()
        if TYPE_CHECKING:
            assert_type(result, tuple[mod.ParallelBackendBase[Any], int])
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestParallelConfig:
    """Test parallel_config class type hints."""

    def test_class_exists(self) -> None:
        """parallel_config should exist in runtime."""
        assert hasattr(mod, "parallel_config")
        assert inspect.isclass(mod.parallel_config)

    def test_init_signature(self) -> None:
        """parallel_config.__init__ should have correct signature."""
        sig = inspect.signature(mod.parallel_config.__init__)
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

    def test_context_manager(self) -> None:
        """parallel_config should work as context manager."""
        with mod.parallel_config() as config:
            assert_type(config, dict[str, Any])
            assert isinstance(config, dict)

    def test_unregister_method(self) -> None:
        """parallel_config.unregister should exist."""
        assert hasattr(mod.parallel_config, "unregister")
        assert callable(mod.parallel_config.unregister)


class TestParallelBackend:
    """Test parallel_backend class type hints."""

    def test_class_exists(self) -> None:
        """parallel_backend should exist in runtime."""
        assert hasattr(mod, "parallel_backend")
        assert inspect.isclass(mod.parallel_backend)

    def test_inherits(self) -> None:
        """parallel_backend should inherit from parallel_config."""
        assert issubclass(mod.parallel_backend, mod.parallel_config)

    def test_init_signature(self) -> None:
        """parallel_backend.__init__ should have correct signature."""
        sig = inspect.signature(mod.parallel_backend.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "backend" in params
        assert "n_jobs" in params
        assert "inner_max_num_threads" in params


class TestBatchedCalls:
    """Test BatchedCalls class type hints."""

    def test_class_exists(self) -> None:
        """BatchedCalls should exist in runtime."""
        assert hasattr(mod, "BatchedCalls")
        assert inspect.isclass(mod.BatchedCalls)

    def test_init_signature(self) -> None:
        """BatchedCalls.__init__ should have correct signature."""
        sig = inspect.signature(mod.BatchedCalls.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "iterator_slice" in params
        assert "backend_and_jobs" in params
        assert "reducer_callback" in params
        assert "pickle_cache" in params

    def test_callable(self) -> None:
        """BatchedCalls instances should be callable."""
        backend, n_jobs = mod.get_active_backend()
        obj = mod.BatchedCalls([], (backend, n_jobs))
        assert callable(obj)

    def test_call_return_type(self) -> None:
        """BatchedCalls.__call__ should return list[Any]."""
        backend, n_jobs = mod.get_active_backend()
        obj = mod.BatchedCalls([], (backend, n_jobs))
        result = obj()
        assert_type(result, list[Any])
        assert isinstance(result, list)

    def test_len_return_type(self) -> None:
        """BatchedCalls.__len__ should return int."""
        backend, n_jobs = mod.get_active_backend()
        obj = mod.BatchedCalls([], (backend, n_jobs))
        result = len(obj)
        assert_type(result, int)
        assert isinstance(result, int)

    def test_items_attribute(self) -> None:
        """BatchedCalls.items should be a list."""
        backend, n_jobs = mod.get_active_backend()
        obj = mod.BatchedCalls([], (backend, n_jobs))
        assert hasattr(obj, "items")
        assert isinstance(obj.items, list)


class TestCpuCount:
    """Test cpu_count function type hints."""

    def test_exists(self) -> None:
        """cpu_count should exist in runtime."""
        assert hasattr(mod, "cpu_count")
        assert callable(mod.cpu_count)

    def test_signature(self) -> None:
        """cpu_count should have correct signature."""
        sig = inspect.signature(mod.cpu_count)
        params = list(sig.parameters.keys())
        assert params == ["only_physical_cores"]

    def test_return_type(self) -> None:
        """cpu_count should return int."""
        result = mod.cpu_count()
        assert_type(result, int)
        assert isinstance(result, int)


class TestDelayed:
    """Test delayed function type hints."""

    def test_exists(self) -> None:
        """delayed should exist in runtime."""
        assert hasattr(mod, "delayed")
        assert callable(mod.delayed)

    def test_signature(self) -> None:
        """delayed should have correct signature."""
        sig = inspect.signature(mod.delayed)
        params = list(sig.parameters.keys())
        assert params == ["function"]

    def test_return_type(self) -> None:
        """delayed should return a callable wrapper."""

        def sample_func(x: int) -> int:
            return x * 2

        wrapper = mod.delayed(sample_func)
        assert callable(wrapper)

    def test_wrapper_return_type(self) -> None:
        """delayed wrapper should return BatchedCall (tuple)."""

        def sample_func(x: int) -> int:
            return x * 2

        wrapper = mod.delayed(sample_func)
        result = wrapper(21)
        # delayed wrapper returns BatchedCall which is a tuple
        assert isinstance(result, tuple)
        assert len(result) == 3
        # First element is the function
        assert callable(result[0])
        # Second element is positional args tuple
        assert isinstance(result[1], tuple)
        # Third element is keyword args dict
        assert isinstance(result[2], dict)


class TestBatchCompletionCallBack:
    """Test BatchCompletionCallBack class type hints."""

    def test_class_exists(self) -> None:
        """BatchCompletionCallBack should exist in runtime."""
        assert hasattr(mod, "BatchCompletionCallBack")
        assert inspect.isclass(mod.BatchCompletionCallBack)

    def test_init_signature(self) -> None:
        """BatchCompletionCallBack.__init__ should have correct signature."""
        sig = inspect.signature(mod.BatchCompletionCallBack.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "dispatch_timestamp" in params
        assert "batch_size" in params
        assert "parallel" in params

    def test_has_call_method(self) -> None:
        """BatchCompletionCallBack should have __call__ method."""
        # Cannot easily instantiate without a Parallel instance
        # Verify that the class has the method defined
        assert hasattr(mod.BatchCompletionCallBack, "__call__")  # noqa: B004

    def test_register_job_method(self) -> None:
        """BatchCompletionCallBack.register_job should exist."""
        sig = inspect.signature(mod.BatchCompletionCallBack.register_job)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "job" in params

    def test_get_result_method(self) -> None:
        """BatchCompletionCallBack.get_result should exist."""
        sig = inspect.signature(mod.BatchCompletionCallBack.get_result)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "timeout" in params

    def test_get_status_method(self) -> None:
        """BatchCompletionCallBack.get_status should exist."""
        sig = inspect.signature(mod.BatchCompletionCallBack.get_status)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "timeout" in params


class TestRegisterParallelBackend:
    """Test register_parallel_backend function type hints."""

    def test_exists(self) -> None:
        """register_parallel_backend should exist in runtime."""
        assert hasattr(mod, "register_parallel_backend")
        assert callable(mod.register_parallel_backend)

    def test_signature(self) -> None:
        """register_parallel_backend should have correct signature."""
        sig = inspect.signature(mod.register_parallel_backend)
        params = list(sig.parameters.keys())
        assert "name" in params
        assert "factory" in params
        assert "make_default" in params


class TestEffectiveNJobs:
    """Test effective_n_jobs function type hints."""

    def test_exists(self) -> None:
        """effective_n_jobs should exist in runtime."""
        assert hasattr(mod, "effective_n_jobs")
        assert callable(mod.effective_n_jobs)

    def test_signature(self) -> None:
        """effective_n_jobs should have correct signature."""
        sig = inspect.signature(mod.effective_n_jobs)
        params = list(sig.parameters.keys())
        assert params == ["n_jobs"]

    def test_return_type(self) -> None:
        """effective_n_jobs should return int."""
        result = mod.effective_n_jobs(1)
        assert_type(result, int)
        assert isinstance(result, int)


class TestParallel:
    """Test Parallel class type hints."""

    def test_class_exists(self) -> None:
        """Parallel should exist in runtime."""
        assert hasattr(mod, "Parallel")
        assert inspect.isclass(mod.Parallel)

    def test_inherits(self) -> None:
        """Parallel should inherit from Logger."""
        assert issubclass(mod.Parallel, mod.Logger)

    def test_init_signature(self) -> None:
        """Parallel.__init__ should have correct signature."""
        sig = inspect.signature(mod.Parallel.__init__)
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

    def test_context_manager(self) -> None:
        """Parallel should work as context manager."""
        with mod.Parallel(n_jobs=1) as parallel:
            if TYPE_CHECKING:
                assert_type(parallel, mod.Parallel[Literal["list"]])
            assert isinstance(parallel, mod.Parallel)

    def test_callable(self) -> None:
        """Parallel instances should be callable."""
        obj = mod.Parallel(n_jobs=1)
        assert callable(obj)

    def test_call_return_type_list(self) -> None:
        """Parallel.__call__ should return list with default return_as."""

        def sample_func(x: int) -> int:
            return x * 2

        parallel = mod.Parallel(n_jobs=1)
        result = parallel(mod.delayed(sample_func)(i) for i in range(3))
        assert_type(result, list[int])
        assert isinstance(result, list)
        assert result == [0, 2, 4]

    def test_dispatch_next_method(self) -> None:
        """Parallel.dispatch_next should exist."""
        sig = inspect.signature(mod.Parallel.dispatch_next)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_dispatch_one_batch_method(self) -> None:
        """Parallel.dispatch_one_batch should exist."""
        sig = inspect.signature(mod.Parallel.dispatch_one_batch)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "iterator" in params

    def test_print_progress_method(self) -> None:
        """Parallel.print_progress should exist."""
        sig = inspect.signature(mod.Parallel.print_progress)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_attributes(self) -> None:
        """Parallel attributes should have correct types."""
        obj = mod.Parallel(n_jobs=1, verbose=0, timeout=None)
        assert_type(obj.verbose, int)
        assert isinstance(obj.verbose, int)
        assert_type(obj.n_jobs, int)
        assert isinstance(obj.n_jobs, int)
