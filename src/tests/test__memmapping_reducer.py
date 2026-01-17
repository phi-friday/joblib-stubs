"""Tests for joblib._memmapping_reducer stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib._memmapping_reducer as mod


class TestConstants:
    """Test module constants."""

    def test_system_shared_mem_fs_exists(self) -> None:
        """SYSTEM_SHARED_MEM_FS should exist."""
        assert hasattr(mod, "SYSTEM_SHARED_MEM_FS")

    def test_system_shared_mem_fs_type(self) -> None:
        """SYSTEM_SHARED_MEM_FS should be str."""
        assert_type(mod.SYSTEM_SHARED_MEM_FS, str)
        assert isinstance(mod.SYSTEM_SHARED_MEM_FS, str)

    def test_system_shared_mem_fs_min_size_exists(self) -> None:
        """SYSTEM_SHARED_MEM_FS_MIN_SIZE should exist."""
        assert hasattr(mod, "SYSTEM_SHARED_MEM_FS_MIN_SIZE")

    def test_system_shared_mem_fs_min_size_type(self) -> None:
        """SYSTEM_SHARED_MEM_FS_MIN_SIZE should be int."""
        assert_type(mod.SYSTEM_SHARED_MEM_FS_MIN_SIZE, int)
        assert isinstance(mod.SYSTEM_SHARED_MEM_FS_MIN_SIZE, int)

    def test_folder_permissions_exists(self) -> None:
        """FOLDER_PERMISSIONS should exist."""
        assert hasattr(mod, "FOLDER_PERMISSIONS")

    def test_folder_permissions_type(self) -> None:
        """FOLDER_PERMISSIONS should be int."""
        assert_type(mod.FOLDER_PERMISSIONS, int)
        assert isinstance(mod.FOLDER_PERMISSIONS, int)

    def test_file_permissions_exists(self) -> None:
        """FILE_PERMISSIONS should exist."""
        assert hasattr(mod, "FILE_PERMISSIONS")

    def test_file_permissions_type(self) -> None:
        """FILE_PERMISSIONS should be int."""
        assert_type(mod.FILE_PERMISSIONS, int)
        assert isinstance(mod.FILE_PERMISSIONS, int)

    def test_joblib_mmaps_exists(self) -> None:
        """JOBLIB_MMAPS should exist."""
        assert hasattr(mod, "JOBLIB_MMAPS")

    def test_joblib_mmaps_type(self) -> None:
        """JOBLIB_MMAPS should be set of str."""
        assert_type(mod.JOBLIB_MMAPS, set[str])
        assert isinstance(mod.JOBLIB_MMAPS, set)


class TestAddMaybeUnlinkFinalizer:
    """Test add_maybe_unlink_finalizer function."""

    def test_exists(self) -> None:
        """add_maybe_unlink_finalizer should exist."""
        assert hasattr(mod, "add_maybe_unlink_finalizer")

    def test_callable(self) -> None:
        """add_maybe_unlink_finalizer should be callable."""
        assert callable(mod.add_maybe_unlink_finalizer)


class TestUnlinkFile:
    """Test unlink_file function."""

    def test_exists(self) -> None:
        """unlink_file should exist."""
        assert hasattr(mod, "unlink_file")

    def test_callable(self) -> None:
        """unlink_file should be callable."""
        assert callable(mod.unlink_file)


class TestHasShareableMemory:
    """Test has_shareable_memory function."""

    def test_exists(self) -> None:
        """has_shareable_memory should exist."""
        assert hasattr(mod, "has_shareable_memory")

    def test_callable(self) -> None:
        """has_shareable_memory should be callable."""
        assert callable(mod.has_shareable_memory)

    def test_signature(self) -> None:
        """has_shareable_memory should have correct signature."""
        sig = inspect.signature(mod.has_shareable_memory)
        params = list(sig.parameters.keys())
        assert "a" in params


class TestReduceArrayMemmapBackward:
    """Test reduce_array_memmap_backward function."""

    def test_exists(self) -> None:
        """reduce_array_memmap_backward should exist."""
        assert hasattr(mod, "reduce_array_memmap_backward")

    def test_callable(self) -> None:
        """reduce_array_memmap_backward should be callable."""
        assert callable(mod.reduce_array_memmap_backward)


class TestArrayMemmapForwardReducer:
    """Test ArrayMemmapForwardReducer class."""

    def test_exists(self) -> None:
        """ArrayMemmapForwardReducer should exist."""
        assert hasattr(mod, "ArrayMemmapForwardReducer")

    def test_is_class(self) -> None:
        """ArrayMemmapForwardReducer should be a class."""
        assert inspect.isclass(mod.ArrayMemmapForwardReducer)

    def test_init_signature(self) -> None:
        """ArrayMemmapForwardReducer.__init__ should have correct signature."""
        sig = inspect.signature(mod.ArrayMemmapForwardReducer.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "max_nbytes" in params
        assert "temp_folder_resolver" in params
        assert "mmap_mode" in params
        assert "unlink_on_gc_collect" in params


class TestGetMemmappingReducers:
    """Test get_memmapping_reducers function."""

    def test_exists(self) -> None:
        """get_memmapping_reducers should exist."""
        assert hasattr(mod, "get_memmapping_reducers")

    def test_callable(self) -> None:
        """get_memmapping_reducers should be callable."""
        assert callable(mod.get_memmapping_reducers)

    def test_signature(self) -> None:
        """get_memmapping_reducers should have correct signature."""
        sig = inspect.signature(mod.get_memmapping_reducers)
        params = list(sig.parameters.keys())
        assert "forward_reducers" in params
        assert "backward_reducers" in params
        assert "temp_folder_resolver" in params
        assert "max_nbytes" in params
        assert "mmap_mode" in params


class TestTemporaryResourcesManager:
    """Test TemporaryResourcesManager class."""

    def test_exists(self) -> None:
        """TemporaryResourcesManager should exist."""
        assert hasattr(mod, "TemporaryResourcesManager")

    def test_is_class(self) -> None:
        """TemporaryResourcesManager should be a class."""
        assert inspect.isclass(mod.TemporaryResourcesManager)

    def test_init_signature(self) -> None:
        """TemporaryResourcesManager.__init__ should have correct signature."""
        sig = inspect.signature(mod.TemporaryResourcesManager.__init__)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "temp_folder_root" in params
        assert "context_id" in params

    def test_methods_exist(self) -> None:
        """TemporaryResourcesManager should have required methods."""
        assert hasattr(mod.TemporaryResourcesManager, "set_current_context")
        assert hasattr(mod.TemporaryResourcesManager, "register_new_context")
        assert hasattr(mod.TemporaryResourcesManager, "resolve_temp_folder_name")
        assert hasattr(mod.TemporaryResourcesManager, "register_folder_finalizer")
