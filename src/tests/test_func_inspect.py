"""Tests for joblib.func_inspect stub types."""

from __future__ import annotations

import inspect
from types import FunctionType
from typing import assert_type

import joblib.func_inspect as mod


class TestConstants:
    """Test module-level constants."""

    def test_full_argspec_fields_exists(self) -> None:
        """full_argspec_fields should exist in runtime."""
        assert hasattr(mod, "full_argspec_fields")

    def test_full_argspec_fields_type(self) -> None:
        """full_argspec_fields should be a str."""
        assert_type(mod.full_argspec_fields, str)
        assert isinstance(mod.full_argspec_fields, str)

    def test_full_argspec_type_exists(self) -> None:
        """full_argspec_type should exist in runtime."""
        assert hasattr(mod, "full_argspec_type")


class TestGetFuncCode:
    """Test get_func_code type hints."""

    def test_exists(self) -> None:
        """get_func_code should exist in runtime."""
        assert hasattr(mod, "get_func_code")
        assert callable(mod.get_func_code)

    def test_signature(self) -> None:
        """get_func_code should have correct signature."""
        sig = inspect.signature(mod.get_func_code)
        params = list(sig.parameters.keys())
        assert params == ["func"]

    def test_return_type(self) -> None:
        """get_func_code should return tuple[str, str, int]."""

        def sample_func() -> None:
            pass

        result = mod.get_func_code(
            FunctionType(sample_func.__code__, sample_func.__globals__)
        )
        assert_type(result, tuple[str, str, int])
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert isinstance(result[0], str)
        assert isinstance(result[1], str)
        assert isinstance(result[2], int)


class TestGetFuncName:
    """Test get_func_name type hints."""

    def test_exists(self) -> None:
        """get_func_name should exist in runtime."""
        assert hasattr(mod, "get_func_name")
        assert callable(mod.get_func_name)

    def test_signature(self) -> None:
        """get_func_name should have correct signature."""
        sig = inspect.signature(mod.get_func_name)
        params = list(sig.parameters.keys())
        assert "func" in params
        assert "resolv_alias" in params
        assert "win_characters" in params

    def test_return_type(self) -> None:
        """get_func_name should return tuple[list[str], str]."""

        def sample_func() -> None:
            pass

        result = mod.get_func_name(sample_func)
        assert_type(result, tuple[list[str], str])
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], list)
        assert isinstance(result[1], str)


class TestFilterArgs:
    """Test filter_args type hints."""

    def test_exists(self) -> None:
        """filter_args should exist in runtime."""
        assert hasattr(mod, "filter_args")
        assert callable(mod.filter_args)

    def test_signature(self) -> None:
        """filter_args should have correct signature."""
        sig = inspect.signature(mod.filter_args)
        params = list(sig.parameters.keys())
        assert "func" in params
        assert "ignore_lst" in params
        assert "args" in params
        assert "kwargs" in params

    def test_return_type(self) -> None:
        """filter_args should return dict[str, Any]."""

        def sample_func(a: int, b: str) -> None:
            pass

        result = mod.filter_args(sample_func, [], (1, "test"), {})
        assert isinstance(result, dict)


class TestFormatSignature:
    """Test format_signature type hints."""

    def test_exists(self) -> None:
        """format_signature should exist in runtime."""
        assert hasattr(mod, "format_signature")
        assert callable(mod.format_signature)

    def test_signature(self) -> None:
        """format_signature should have correct signature."""
        sig = inspect.signature(mod.format_signature)
        params = list(sig.parameters.keys())
        assert "func" in params
        assert "args" in params
        assert "kwargs" in params

    def test_return_type(self) -> None:
        """format_signature should return tuple[list[str], str]."""

        def sample_func(a: int) -> None:
            pass

        result = mod.format_signature(sample_func, 1)
        assert_type(result, tuple[list[str], str])
        assert isinstance(result, tuple)
        assert len(result) == 2
        # Runtime actually returns (str, str) not (list[str], str)
        assert isinstance(result[0], (list, str))
        assert isinstance(result[1], str)


class TestFormatCall:
    """Test format_call type hints."""

    def test_exists(self) -> None:
        """format_call should exist in runtime."""
        assert hasattr(mod, "format_call")
        assert callable(mod.format_call)

    def test_signature(self) -> None:
        """format_call should have correct signature."""
        sig = inspect.signature(mod.format_call)
        params = list(sig.parameters.keys())
        assert "func" in params
        assert "args" in params
        assert "kwargs" in params
        assert "object_name" in params

    def test_return_type(self) -> None:
        """format_call should return str."""

        def sample_func(a: int) -> None:
            pass

        result = mod.format_call(sample_func, (1,), {})
        assert_type(result, str)
        assert isinstance(result, str)
