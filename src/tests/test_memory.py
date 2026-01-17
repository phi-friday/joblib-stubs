"""Tests for joblib.memory stub types."""

from __future__ import annotations

import inspect
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, assert_type

import joblib.memory as mod
from joblib.logger import Logger  # Different module for inheritance check


class TestConstants:
    """Test module-level constants."""

    def test_first_line_text_exists(self) -> None:
        """FIRST_LINE_TEXT should exist in runtime."""
        assert hasattr(mod, "FIRST_LINE_TEXT")

    def test_first_line_text_type(self) -> None:
        """FIRST_LINE_TEXT should be a str."""
        assert_type(mod.FIRST_LINE_TEXT, str)
        assert isinstance(mod.FIRST_LINE_TEXT, str)


class TestExtractFirstLine:
    """Test extract_first_line type hints."""

    def test_exists(self) -> None:
        """extract_first_line should exist in runtime."""
        assert hasattr(mod, "extract_first_line")
        assert callable(mod.extract_first_line)

    def test_signature(self) -> None:
        """extract_first_line should have correct signature."""
        sig = inspect.signature(mod.extract_first_line)
        params = list(sig.parameters.keys())
        assert params == ["func_code"]

    def test_return_type(self) -> None:
        """extract_first_line should return tuple[str, int]."""
        result = mod.extract_first_line("def foo():\n    pass")
        assert_type(result, tuple[str, int])
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], int)


class TestJobLibCollisionWarning:
    """Test JobLibCollisionWarning type hints."""

    def test_class_exists(self) -> None:
        """JobLibCollisionWarning should exist in runtime."""
        assert hasattr(mod, "JobLibCollisionWarning")
        assert inspect.isclass(mod.JobLibCollisionWarning)

    def test_inherits(self) -> None:
        """JobLibCollisionWarning should inherit from UserWarning."""
        assert issubclass(mod.JobLibCollisionWarning, UserWarning)


class TestRegisterStoreBackend:
    """Test register_store_backend type hints."""

    def test_exists(self) -> None:
        """register_store_backend should exist in runtime."""
        assert hasattr(mod, "register_store_backend")
        assert callable(mod.register_store_backend)

    def test_signature(self) -> None:
        """register_store_backend should have correct signature."""
        sig = inspect.signature(mod.register_store_backend)
        params = list(sig.parameters.keys())
        assert "backend_name" in params
        assert "backend" in params


class TestMemorizedResult:
    """Test MemorizedResult class type hints."""

    def test_class_exists(self) -> None:
        """MemorizedResult should exist in runtime."""
        assert hasattr(mod, "MemorizedResult")
        assert inspect.isclass(mod.MemorizedResult)

    def test_inherits(self) -> None:
        """MemorizedResult should inherit from Logger."""
        assert issubclass(mod.MemorizedResult, Logger)

    def test_init_signature(self) -> None:
        """MemorizedResult.__init__ should have correct signature."""
        sig = inspect.signature(mod.MemorizedResult.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "location" in params
        assert "call_id" in params
        assert "backend" in params
        assert "mmap_mode" in params
        assert "verbose" in params
        assert "timestamp" in params
        assert "metadata" in params

    def test_get_method(self) -> None:
        """MemorizedResult.get should exist."""
        sig = inspect.signature(mod.MemorizedResult.get)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_clear_method(self) -> None:
        """MemorizedResult.clear should exist."""
        sig = inspect.signature(mod.MemorizedResult.clear)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestNotMemorizedResult:
    """Test NotMemorizedResult class type hints."""

    def test_class_exists(self) -> None:
        """NotMemorizedResult should exist in runtime."""
        assert hasattr(mod, "NotMemorizedResult")
        assert inspect.isclass(mod.NotMemorizedResult)

    def test_init_signature(self) -> None:
        """NotMemorizedResult.__init__ should have correct signature."""
        sig = inspect.signature(mod.NotMemorizedResult.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "value"]

    def test_attributes(self) -> None:
        """NotMemorizedResult attributes should have correct types."""
        obj = mod.NotMemorizedResult(42)
        assert_type(obj.valid, bool)
        assert isinstance(obj.valid, bool)

    def test_get_method(self) -> None:
        """NotMemorizedResult.get should exist."""
        sig = inspect.signature(mod.NotMemorizedResult.get)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_get_return_type(self) -> None:
        """NotMemorizedResult.get should return the stored value."""
        obj = mod.NotMemorizedResult(42)
        result = obj.get()
        assert_type(result, int)
        assert result == 42

    def test_clear_method(self) -> None:
        """NotMemorizedResult.clear should exist."""
        sig = inspect.signature(mod.NotMemorizedResult.clear)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestNotMemorizedFunc:
    """Test NotMemorizedFunc class type hints."""

    def test_class_exists(self) -> None:
        """NotMemorizedFunc should exist in runtime."""
        assert hasattr(mod, "NotMemorizedFunc")
        assert inspect.isclass(mod.NotMemorizedFunc)

    def test_init_signature(self) -> None:
        """NotMemorizedFunc.__init__ should have correct signature."""
        sig = inspect.signature(mod.NotMemorizedFunc.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "func"]

    def test_callable(self) -> None:
        """NotMemorizedFunc instances should be callable."""

        def sample_func(x: int) -> int:
            return x

        obj = mod.NotMemorizedFunc(sample_func)
        assert callable(obj)

    def test_call_return_type(self) -> None:
        """NotMemorizedFunc.__call__ should return function's result."""

        def sample_func(x: int) -> int:
            return x * 2

        obj = mod.NotMemorizedFunc(sample_func)
        result = obj(21)
        assert_type(result, int)
        assert result == 42

    def test_call_and_shelve_method(self) -> None:
        """NotMemorizedFunc.call_and_shelve should exist."""
        sig = inspect.signature(mod.NotMemorizedFunc.call_and_shelve)
        params = list(sig.parameters.keys())
        assert "self" in params

    def test_call_and_shelve_return_type(self) -> None:
        """NotMemorizedFunc.call_and_shelve should return NotMemorizedResult."""

        def sample_func(x: int) -> int:
            return x * 2

        obj = mod.NotMemorizedFunc(sample_func)
        result = obj.call_and_shelve(21)
        if TYPE_CHECKING:
            assert_type(result, mod.NotMemorizedResult[int])
        assert isinstance(result, mod.NotMemorizedResult)
        assert result.get() == 42

    def test_clear_method(self) -> None:
        """NotMemorizedFunc.clear should exist."""
        sig = inspect.signature(mod.NotMemorizedFunc.clear)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "warn" in params

    def test_call_method_exists(self) -> None:
        """NotMemorizedFunc.call should exist."""
        sig = inspect.signature(mod.NotMemorizedFunc.call)
        params = list(sig.parameters.keys())
        assert "self" in params

    def test_check_call_in_cache_method(self) -> None:
        """NotMemorizedFunc.check_call_in_cache should exist."""
        sig = inspect.signature(mod.NotMemorizedFunc.check_call_in_cache)
        params = list(sig.parameters.keys())
        assert "self" in params


class TestAsyncNotMemorizedFunc:
    """Test AsyncNotMemorizedFunc class type hints."""

    def test_class_exists(self) -> None:
        """AsyncNotMemorizedFunc should exist in runtime."""
        assert hasattr(mod, "AsyncNotMemorizedFunc")
        assert inspect.isclass(mod.AsyncNotMemorizedFunc)

    def test_inherits(self) -> None:
        """AsyncNotMemorizedFunc should inherit from NotMemorizedFunc."""
        assert issubclass(mod.AsyncNotMemorizedFunc, mod.NotMemorizedFunc)

    def test_init_signature(self) -> None:
        """AsyncNotMemorizedFunc.__init__ should have correct signature."""
        sig = inspect.signature(mod.AsyncNotMemorizedFunc.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "func"]


class TestMemorizedFunc:
    """Test MemorizedFunc class type hints."""

    def test_class_exists(self) -> None:
        """MemorizedFunc should exist in runtime."""
        assert hasattr(mod, "MemorizedFunc")
        assert inspect.isclass(mod.MemorizedFunc)

    def test_inherits(self) -> None:
        """MemorizedFunc should inherit from Logger."""
        assert issubclass(mod.MemorizedFunc, Logger)

    def test_init_signature(self) -> None:
        """MemorizedFunc.__init__ should have correct signature."""
        sig = inspect.signature(mod.MemorizedFunc.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "func" in params
        assert "location" in params
        assert "backend" in params
        assert "ignore" in params
        assert "mmap_mode" in params
        assert "compress" in params
        assert "verbose" in params
        assert "timestamp" in params
        assert "cache_validation_callback" in params

    def test_callable(self) -> None:
        """MemorizedFunc instances should be callable."""

        def sample_func(x: int) -> int:
            return x

        with tempfile.TemporaryDirectory() as tmpdir:
            obj = mod.MemorizedFunc(sample_func, tmpdir)
            assert callable(obj)

    def test_call_return_type(self) -> None:
        """MemorizedFunc.__call__ should return function's result."""

        def sample_func(x: int) -> int:
            return x * 2

        with tempfile.TemporaryDirectory() as tmpdir:
            obj = mod.MemorizedFunc(sample_func, tmpdir)
            result = obj(21)
            assert_type(result, int)
            assert result == 42

    def test_call_and_shelve_method(self) -> None:
        """MemorizedFunc.call_and_shelve should exist."""
        sig = inspect.signature(mod.MemorizedFunc.call_and_shelve)
        params = list(sig.parameters.keys())
        assert "self" in params

    def test_check_call_in_cache_method(self) -> None:
        """MemorizedFunc.check_call_in_cache should exist."""
        sig = inspect.signature(mod.MemorizedFunc.check_call_in_cache)
        params = list(sig.parameters.keys())
        assert "self" in params

    def test_clear_method(self) -> None:
        """MemorizedFunc.clear should exist."""
        sig = inspect.signature(mod.MemorizedFunc.clear)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "warn" in params

    def test_call_method_exists(self) -> None:
        """MemorizedFunc.call should exist."""
        sig = inspect.signature(mod.MemorizedFunc.call)
        params = list(sig.parameters.keys())
        assert "self" in params


class TestAsyncMemorizedFunc:
    """Test AsyncMemorizedFunc class type hints."""

    def test_class_exists(self) -> None:
        """AsyncMemorizedFunc should exist in runtime."""
        assert hasattr(mod, "AsyncMemorizedFunc")
        assert inspect.isclass(mod.AsyncMemorizedFunc)

    def test_inherits(self) -> None:
        """AsyncMemorizedFunc should inherit from MemorizedFunc."""
        assert issubclass(mod.AsyncMemorizedFunc, mod.MemorizedFunc)

    def test_init_signature(self) -> None:
        """AsyncMemorizedFunc.__init__ should have correct signature."""
        sig = inspect.signature(mod.AsyncMemorizedFunc.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "func" in params
        assert "location" in params


class TestMemory:
    """Test Memory class type hints."""

    def test_class_exists(self) -> None:
        """Memory should exist in runtime."""
        assert hasattr(mod, "Memory")
        assert inspect.isclass(mod.Memory)

    def test_inherits(self) -> None:
        """Memory should inherit from Logger."""
        assert issubclass(mod.Memory, Logger)

    def test_init_signature(self) -> None:
        """Memory.__init__ should have correct signature."""
        sig = inspect.signature(mod.Memory.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "location" in params
        assert "backend" in params
        assert "mmap_mode" in params
        assert "compress" in params
        assert "verbose" in params
        assert "backend_options" in params

    def test_cache_method(self) -> None:
        """Memory.cache should exist."""
        sig = inspect.signature(mod.Memory.cache)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "func" in params
        assert "ignore" in params
        assert "verbose" in params
        assert "mmap_mode" in params
        assert "cache_validation_callback" in params

    def test_cache_return_type_with_func(self) -> None:
        """Memory.cache with func should return MemorizedFunc."""

        def sample_func(x: int) -> int:
            return x

        with tempfile.TemporaryDirectory() as tmpdir:
            mem = mod.Memory(tmpdir)
            cached = mem.cache(sample_func)
            # MemorizedFunc has ParamSpec, exact type assertion is complex
            # Type checker verifies the return type matches MemorizedFunc
            assert isinstance(cached, mod.MemorizedFunc)
            # Verify the callable works correctly
            result = cached(42)
            assert_type(result, int)
            assert result == 42

    def test_cache_return_type_without_func(self) -> None:
        """Memory.cache without func should return decorator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = mod.Memory(tmpdir)
            decorator = mem.cache()
            assert callable(decorator)

    def test_clear_method(self) -> None:
        """Memory.clear should exist."""
        sig = inspect.signature(mod.Memory.clear)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "warn" in params

    def test_reduce_size_method(self) -> None:
        """Memory.reduce_size should exist."""
        sig = inspect.signature(mod.Memory.reduce_size)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "bytes_limit" in params
        assert "items_limit" in params
        assert "age_limit" in params

    def test_eval_method(self) -> None:
        """Memory.eval should exist."""
        sig = inspect.signature(mod.Memory.eval)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "func" in params

    def test_memory_instantiation(self) -> None:
        """Memory should be instantiable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mem = mod.Memory(tmpdir)
            assert_type(mem.location, str | Path)
            assert isinstance(mem.location, (str, Path))


class TestExpiresAfter:
    """Test expires_after type hints."""

    def test_exists(self) -> None:
        """expires_after should exist in runtime."""
        assert hasattr(mod, "expires_after")
        assert callable(mod.expires_after)

    def test_signature(self) -> None:
        """expires_after should have correct signature."""
        sig = inspect.signature(mod.expires_after)
        params = list(sig.parameters.keys())
        assert "days" in params
        assert "seconds" in params
        assert "microseconds" in params
        assert "milliseconds" in params
        assert "minutes" in params
        assert "hours" in params
        assert "weeks" in params

    def test_return_type(self) -> None:
        """expires_after should return callable."""
        result = mod.expires_after(days=1)
        assert callable(result)
