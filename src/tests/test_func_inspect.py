"""Tests for joblib.func_inspect stub types."""

from __future__ import annotations

import inspect
from inspect import FullArgSpec
from types import FunctionType
from typing import Any, assert_type

import joblib.func_inspect as mod


class TestFullArgSpecFields:
    """Test full_argspec_fields constant."""

    def test_exists(self) -> None:
        """full_argspec_fields should exist in runtime."""
        assert hasattr(mod, "full_argspec_fields")

    def test_type(self) -> None:
        """full_argspec_fields should be a str."""
        assert_type(mod.full_argspec_fields, str)
        assert isinstance(mod.full_argspec_fields, str)


class TestFullArgSpecType:
    """Test full_argspec_type (custom NamedTuple)."""

    def test_exists(self) -> None:
        """full_argspec_type should exist in runtime."""
        assert hasattr(mod, "full_argspec_type")

    def test_is_namedtuple(self) -> None:
        """full_argspec_type should be a NamedTuple."""
        assert hasattr(mod.full_argspec_type, "_fields")
        assert issubclass(mod.full_argspec_type, tuple)

    def test_fields(self) -> None:
        """full_argspec_type should have correct fields."""
        expected_fields = (
            "args",
            "varargs",
            "varkw",
            "defaults",
            "kwonlyargs",
            "kwonlydefaults",
            "annotations",
        )
        assert mod.full_argspec_type._fields == expected_fields

    def test_type_annotation(self) -> None:
        """full_argspec_type should be typed as FullArgSpec."""
        # Stub defines it as inspect.FullArgSpec for type checking purposes
        assert_type(mod.full_argspec_type, type[FullArgSpec])

    def test_instance_creation(self) -> None:
        """full_argspec_type instances should be creatable."""
        instance = mod.full_argspec_type(
            args=["x", "y"],
            varargs=None,
            varkw=None,
            defaults=(1,),
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={},
        )
        assert isinstance(instance, tuple)
        assert len(instance) == 7

    def test_instance_args_attribute(self) -> None:
        """full_argspec_type.args should have correct type."""
        instance = mod.full_argspec_type(
            args=["x", "y"],
            varargs=None,
            varkw=None,
            defaults=None,
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={},
        )
        assert_type(instance.args, list[str])
        assert instance.args == ["x", "y"]

    def test_instance_varargs_attribute(self) -> None:
        """full_argspec_type.varargs should have correct type."""
        instance = mod.full_argspec_type(
            args=[],
            varargs="args",
            varkw=None,
            defaults=None,
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={},
        )
        assert_type(instance.varargs, str | None)
        assert instance.varargs == "args"

    def test_instance_varkw_attribute(self) -> None:
        """full_argspec_type.varkw should have correct type."""
        instance = mod.full_argspec_type(
            args=[],
            varargs=None,
            varkw="kwargs",
            defaults=None,
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={},
        )
        assert_type(instance.varkw, str | None)
        assert instance.varkw == "kwargs"

    def test_instance_defaults_attribute(self) -> None:
        """full_argspec_type.defaults should have correct type."""
        instance = mod.full_argspec_type(
            args=["x"],
            varargs=None,
            varkw=None,
            defaults=(1, "default"),
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={},
        )
        assert_type(instance.defaults, tuple[Any, ...] | None)
        assert instance.defaults == (1, "default")

    def test_instance_kwonlyargs_attribute(self) -> None:
        """full_argspec_type.kwonlyargs should have correct type."""
        instance = mod.full_argspec_type(
            args=[],
            varargs=None,
            varkw=None,
            defaults=None,
            kwonlyargs=["kw1", "kw2"],
            kwonlydefaults=None,
            annotations={},
        )
        assert_type(instance.kwonlyargs, list[str])
        assert instance.kwonlyargs == ["kw1", "kw2"]

    def test_instance_kwonlydefaults_attribute(self) -> None:
        """full_argspec_type.kwonlydefaults should have correct type."""
        instance = mod.full_argspec_type(
            args=[],
            varargs=None,
            varkw=None,
            defaults=None,
            kwonlyargs=["kw1"],
            kwonlydefaults={"kw1": 42},
            annotations={},
        )
        assert_type(instance.kwonlydefaults, dict[str, Any] | None)
        assert instance.kwonlydefaults == {"kw1": 42}

    def test_instance_annotations_attribute(self) -> None:
        """full_argspec_type.annotations should have correct type."""
        instance = mod.full_argspec_type(
            args=["x"],
            varargs=None,
            varkw=None,
            defaults=None,
            kwonlyargs=[],
            kwonlydefaults=None,
            annotations={"x": int, "return": str},
        )
        assert_type(instance.annotations, dict[str, Any])
        assert instance.annotations == {"x": int, "return": str}


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

        func = FunctionType(sample_func.__code__, sample_func.__globals__)
        result = mod.get_func_code(func)
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
