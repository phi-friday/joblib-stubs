"""Tests for joblib.pool stub types."""

from __future__ import annotations

import inspect
from multiprocessing import get_context
from multiprocessing.pool import Pool
from pickle import Pickler
from typing import assert_type

import joblib.pool as mod


class TestCustomizablePickler:
    """Test CustomizablePickler class type hints."""

    def test_class_exists(self) -> None:
        """CustomizablePickler should exist in runtime."""
        assert hasattr(mod, "CustomizablePickler")
        assert inspect.isclass(mod.CustomizablePickler)

    def test_inherits(self) -> None:
        """CustomizablePickler should inherit from Pickler."""
        assert issubclass(mod.CustomizablePickler, Pickler)

    def test_init_signature(self) -> None:
        """CustomizablePickler.__init__ should have correct signature."""
        sig = inspect.signature(mod.CustomizablePickler.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "writer" in params
        assert "reducers" in params
        assert "protocol" in params

    def test_register_method(self) -> None:
        """CustomizablePickler.register should exist."""
        sig = inspect.signature(mod.CustomizablePickler.register)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "type" in params
        assert "reduce_func" in params


class TestCustomizablePicklingQueue:
    """Test CustomizablePicklingQueue class type hints."""

    def test_class_exists(self) -> None:
        """CustomizablePicklingQueue should exist in runtime."""
        assert hasattr(mod, "CustomizablePicklingQueue")
        assert inspect.isclass(mod.CustomizablePicklingQueue)

    def test_init_signature(self) -> None:
        """CustomizablePicklingQueue.__init__ should have correct signature."""
        sig = inspect.signature(mod.CustomizablePicklingQueue.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "context" in params
        assert "reducers" in params

    def test_empty_method(self) -> None:
        """CustomizablePicklingQueue.empty should exist."""
        sig = inspect.signature(mod.CustomizablePicklingQueue.empty)
        params = list(sig.parameters.keys())
        assert params == ["self"]

    def test_empty_return_type(self) -> None:
        """CustomizablePicklingQueue.empty should return bool."""
        ctx = get_context("spawn")
        obj = mod.CustomizablePicklingQueue(ctx)
        result = obj.empty()
        assert_type(result, bool)
        assert isinstance(result, bool)


class TestPicklingPool:
    """Test PicklingPool class type hints."""

    def test_class_exists(self) -> None:
        """PicklingPool should exist in runtime."""
        assert hasattr(mod, "PicklingPool")
        assert inspect.isclass(mod.PicklingPool)

    def test_inherits(self) -> None:
        """PicklingPool should inherit from Pool."""
        assert issubclass(mod.PicklingPool, Pool)

    def test_init_signature(self) -> None:
        """PicklingPool.__init__ should have correct signature."""
        sig = inspect.signature(mod.PicklingPool.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "processes" in params
        assert "forward_reducers" in params
        assert "backward_reducers" in params


class TestMemmappingPool:
    """Test MemmappingPool class type hints."""

    def test_class_exists(self) -> None:
        """MemmappingPool should exist in runtime."""
        assert hasattr(mod, "MemmappingPool")
        assert inspect.isclass(mod.MemmappingPool)

    def test_inherits(self) -> None:
        """MemmappingPool should inherit from PicklingPool."""
        assert issubclass(mod.MemmappingPool, mod.PicklingPool)

    def test_init_signature(self) -> None:
        """MemmappingPool.__init__ should have correct signature."""
        sig = inspect.signature(mod.MemmappingPool.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "processes" in params
        assert "temp_folder" in params
        assert "max_nbytes" in params
        assert "mmap_mode" in params
        assert "forward_reducers" in params
        assert "backward_reducers" in params
        assert "verbose" in params
        assert "prewarm" in params

    def test_terminate_method(self) -> None:
        """MemmappingPool.terminate should exist."""
        sig = inspect.signature(mod.MemmappingPool.terminate)
        params = list(sig.parameters.keys())
        assert params == ["self"]


class TestModuleReExports:
    """Test module re-exports."""

    def test_get_memmapping_reducers_exists(self) -> None:
        """get_memmapping_reducers should be re-exported."""
        assert hasattr(mod, "get_memmapping_reducers")
        assert callable(mod.get_memmapping_reducers)

    def test_temporary_resources_manager_exists(self) -> None:
        """TemporaryResourcesManager should be re-exported."""
        assert hasattr(mod, "TemporaryResourcesManager")
        assert inspect.isclass(mod.TemporaryResourcesManager)

    def test_assert_spawning_exists(self) -> None:
        """assert_spawning should be re-exported."""
        assert hasattr(mod, "assert_spawning")
        assert callable(mod.assert_spawning)

    def test_mp_exists(self) -> None:
        """mp should be re-exported."""
        assert hasattr(mod, "mp")
