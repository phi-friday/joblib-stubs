"""Tests for joblib.pool stub types."""

from __future__ import annotations

import inspect
from multiprocessing.pool import Pool

import joblib.pool as pool_runtime
from joblib.pool import (
    CustomizablePickler,
    CustomizablePicklingQueue,
    MemmappingPool,
    PicklingPool,
)


class TestCustomizablePickler:
    """Test CustomizablePickler class type hints."""

    def test_class_exists(self) -> None:
        """CustomizablePickler should exist in runtime."""
        assert hasattr(pool_runtime, "CustomizablePickler")
        assert inspect.isclass(pool_runtime.CustomizablePickler)

    def test_init_signature(self) -> None:
        """CustomizablePickler.__init__ should have correct signature."""
        sig = inspect.signature(CustomizablePickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "writer" in params
        assert "reducers" in params
        assert "protocol" in params

    def test_register_method(self) -> None:
        """CustomizablePickler.register should exist."""
        sig = inspect.signature(CustomizablePickler.register)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "type" in params
        assert "reduce_func" in params


class TestCustomizablePicklingQueue:
    """Test CustomizablePicklingQueue class type hints."""

    def test_class_exists(self) -> None:
        """CustomizablePicklingQueue should exist in runtime."""
        assert hasattr(pool_runtime, "CustomizablePicklingQueue")
        assert inspect.isclass(pool_runtime.CustomizablePicklingQueue)

    def test_init_signature(self) -> None:
        """CustomizablePicklingQueue.__init__ should have correct signature."""
        sig = inspect.signature(CustomizablePicklingQueue.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "context" in params
        assert "reducers" in params

    def test_empty_method(self) -> None:
        """CustomizablePicklingQueue.empty should exist."""
        sig = inspect.signature(CustomizablePicklingQueue.empty)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestPicklingPool:
    """Test PicklingPool class type hints."""

    def test_class_exists(self) -> None:
        """PicklingPool should exist in runtime."""
        assert hasattr(pool_runtime, "PicklingPool")
        assert inspect.isclass(pool_runtime.PicklingPool)

    def test_inherits(self) -> None:
        """PicklingPool should inherit from Pool."""
        assert issubclass(PicklingPool, Pool)

    def test_init_signature(self) -> None:
        """PicklingPool.__init__ should have correct signature."""
        sig = inspect.signature(PicklingPool.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "processes" in params
        assert "forward_reducers" in params
        assert "backward_reducers" in params
        assert "kwargs" in params


class TestMemmappingPool:
    """Test MemmappingPool class type hints."""

    def test_class_exists(self) -> None:
        """MemmappingPool should exist in runtime."""
        assert hasattr(pool_runtime, "MemmappingPool")
        assert inspect.isclass(pool_runtime.MemmappingPool)

    def test_inherits(self) -> None:
        """MemmappingPool should inherit from PicklingPool."""
        assert issubclass(MemmappingPool, PicklingPool)

    def test_init_signature(self) -> None:
        """MemmappingPool.__init__ should have correct signature."""
        sig = inspect.signature(MemmappingPool.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "processes" in params
        assert "temp_folder" in params
        assert "max_nbytes" in params
        assert "mmap_mode" in params
        assert "forward_reducers" in params
        assert "backward_reducers" in params
        assert "verbose" in params
        # context_id and prewarm may not be in runtime
        assert "kwargs" in params

    def test_terminate_method(self) -> None:
        """MemmappingPool.terminate should exist."""
        sig = inspect.signature(MemmappingPool.terminate)
        params = list(sig.parameters.keys())
        assert params == ["self"]
