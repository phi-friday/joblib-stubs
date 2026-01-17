"""Tests for joblib.logger stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.logger as mod


class TestFormatTime:
    """Test format_time type hints."""

    def test_exists(self) -> None:
        """format_time should exist in runtime."""
        assert hasattr(mod, "format_time")
        assert callable(mod.format_time)

    def test_signature(self) -> None:
        """format_time should have correct signature."""
        sig = inspect.signature(mod.format_time)
        params = list(sig.parameters.keys())
        assert params == ["t"]

    def test_return_type(self) -> None:
        """format_time should return str."""
        result = mod.format_time(1.5)
        assert_type(result, str)
        assert isinstance(result, str)


class TestShortFormatTime:
    """Test short_format_time type hints."""

    def test_exists(self) -> None:
        """short_format_time should exist in runtime."""
        assert hasattr(mod, "short_format_time")
        assert callable(mod.short_format_time)

    def test_signature(self) -> None:
        """short_format_time should have correct signature."""
        sig = inspect.signature(mod.short_format_time)
        params = list(sig.parameters.keys())
        assert params == ["t"]

    def test_return_type(self) -> None:
        """short_format_time should return str."""
        result = mod.short_format_time(1.5)
        assert_type(result, str)
        assert isinstance(result, str)


class TestPformat:
    """Test pformat type hints."""

    def test_exists(self) -> None:
        """pformat should exist in runtime."""
        assert hasattr(mod, "pformat")
        assert callable(mod.pformat)

    def test_signature(self) -> None:
        """pformat should have correct signature."""
        sig = inspect.signature(mod.pformat)
        params = list(sig.parameters.keys())
        assert "obj" in params
        assert "indent" in params
        assert "depth" in params

    def test_return_type(self) -> None:
        """pformat should return str."""
        result = mod.pformat({"key": "value"})
        assert_type(result, str)
        assert isinstance(result, str)


class TestLogger:
    """Test Logger class type hints."""

    def test_class_exists(self) -> None:
        """Logger should exist in runtime."""
        assert hasattr(mod, "Logger")
        assert inspect.isclass(mod.Logger)

    def test_init_signature(self) -> None:
        """Logger.__init__ should have correct signature."""
        sig = inspect.signature(mod.Logger.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "depth" in params
        assert "name" in params

    def test_attributes(self) -> None:
        """Logger attributes should have correct types."""
        obj = mod.Logger()
        assert_type(obj.depth, int | None)
        assert isinstance(obj.depth, (int, type(None)))

    def test_warn_method(self) -> None:
        """Logger.warn should exist."""
        sig = inspect.signature(mod.Logger.warn)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "msg" in params

    def test_info_method(self) -> None:
        """Logger.info should exist."""
        sig = inspect.signature(mod.Logger.info)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "msg" in params

    def test_debug_method(self) -> None:
        """Logger.debug should exist."""
        sig = inspect.signature(mod.Logger.debug)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "msg" in params

    def test_format_method(self) -> None:
        """Logger.format should exist."""
        sig = inspect.signature(mod.Logger.format)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "obj" in params
        assert "indent" in params

    def test_format_return_type(self) -> None:
        """Logger.format should return str."""
        logger = mod.Logger()
        result = logger.format({"test": 1})
        assert_type(result, str)
        assert isinstance(result, str)


class TestPrintTime:
    """Test PrintTime class type hints."""

    def test_class_exists(self) -> None:
        """PrintTime should exist in runtime."""
        assert hasattr(mod, "PrintTime")
        assert inspect.isclass(mod.PrintTime)

    def test_init_signature(self) -> None:
        """PrintTime.__init__ should have correct signature."""
        sig = inspect.signature(mod.PrintTime.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "logfile" in params
        assert "logdir" in params

    def test_attributes(self) -> None:
        """PrintTime attributes should have correct types."""
        obj = mod.PrintTime()
        assert_type(obj.last_time, float)
        assert isinstance(obj.last_time, float)
        assert_type(obj.start_time, float)
        assert isinstance(obj.start_time, float)
        # logfile can be None when no logfile/logdir specified
        assert_type(obj.logfile, str)
        assert isinstance(obj.logfile, (str, type(None)))

    def test_call_method(self) -> None:
        """PrintTime.__call__ should exist."""
        sig = inspect.signature(mod.PrintTime.__call__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "msg" in params
        assert "total" in params

    def test_callable(self) -> None:
        """PrintTime instances should be callable."""
        obj = mod.PrintTime()
        assert callable(obj)
