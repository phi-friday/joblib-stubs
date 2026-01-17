"""Tests for joblib._utils stub types."""

from __future__ import annotations

import inspect

import joblib._utils as mod


class TestOperators:
    """Test operators variable."""

    def test_exists(self) -> None:
        """operators should exist."""
        assert hasattr(mod, "operators")

    def test_type(self) -> None:
        """operators should be a dict."""
        assert isinstance(mod.operators, dict)


class TestEvalExpr:
    """Test eval_expr function."""

    def test_exists(self) -> None:
        """eval_expr should exist."""
        assert hasattr(mod, "eval_expr")

    def test_callable(self) -> None:
        """eval_expr should be callable."""
        assert callable(mod.eval_expr)

    def test_signature(self) -> None:
        """eval_expr should have correct signature."""
        sig = inspect.signature(mod.eval_expr)
        params = list(sig.parameters.keys())
        assert "expr" in params

    def test_evaluates_simple_expr(self) -> None:
        """eval_expr should evaluate simple expressions."""
        result = mod.eval_expr("1 + 2")
        assert result == 3


class TestLimit:
    """Test limit function."""

    def test_exists(self) -> None:
        """limit should exist."""
        assert hasattr(mod, "limit")

    def test_callable(self) -> None:
        """limit should be callable."""
        assert callable(mod.limit)

    def test_signature(self) -> None:
        """limit should have correct signature."""
        sig = inspect.signature(mod.limit)
        params = list(sig.parameters.keys())
        assert "max_" in params


class TestEval:
    """Test eval_ function."""

    def test_exists(self) -> None:
        """eval_ should exist."""
        assert hasattr(mod, "eval_")

    def test_callable(self) -> None:
        """eval_ should be callable."""
        assert callable(mod.eval_)

    def test_signature(self) -> None:
        """eval_ should have correct signature."""
        sig = inspect.signature(mod.eval_)
        params = list(sig.parameters.keys())
        assert "node" in params
