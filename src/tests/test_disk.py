"""Tests for joblib.disk stub types."""

from __future__ import annotations

import inspect
import tempfile
from pathlib import Path
from typing import assert_type

import joblib.disk as disk_runtime
from joblib.disk import (
    RM_SUBDIRS_N_RETRY,
    RM_SUBDIRS_RETRY_TIME,
    delete_folder,
    disk_used,
    memstr_to_bytes,
    mkdirp,
    rm_subdirs,
)


class TestConstants:
    """Test module-level constants."""

    def test_rm_subdirs_retry_time_exists(self) -> None:
        """RM_SUBDIRS_RETRY_TIME should exist in runtime."""
        assert hasattr(disk_runtime, "RM_SUBDIRS_RETRY_TIME")

    def test_rm_subdirs_retry_time_type(self) -> None:
        """RM_SUBDIRS_RETRY_TIME should be a float."""
        assert_type(RM_SUBDIRS_RETRY_TIME, float)
        assert isinstance(RM_SUBDIRS_RETRY_TIME, float)

    def test_rm_subdirs_n_retry_exists(self) -> None:
        """RM_SUBDIRS_N_RETRY should exist in runtime."""
        assert hasattr(disk_runtime, "RM_SUBDIRS_N_RETRY")

    def test_rm_subdirs_n_retry_type(self) -> None:
        """RM_SUBDIRS_N_RETRY should be an int."""
        assert_type(RM_SUBDIRS_N_RETRY, int)
        assert isinstance(RM_SUBDIRS_N_RETRY, int)


class TestDiskUsed:
    """Test disk_used type hints."""

    def test_exists(self) -> None:
        """disk_used should exist in runtime."""
        assert hasattr(disk_runtime, "disk_used")
        assert callable(disk_runtime.disk_used)

    def test_signature(self) -> None:
        """disk_used should have correct signature."""
        sig = inspect.signature(disk_used)
        params = list(sig.parameters.keys())
        assert params == ["path"]

    def test_return_type(self) -> None:
        """disk_used should return int."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = disk_used(tmpdir)
            assert_type(result, int)
            assert isinstance(result, int)


class TestMemstrToBytes:
    """Test memstr_to_bytes type hints."""

    def test_exists(self) -> None:
        """memstr_to_bytes should exist in runtime."""
        assert hasattr(disk_runtime, "memstr_to_bytes")
        assert callable(disk_runtime.memstr_to_bytes)

    def test_signature(self) -> None:
        """memstr_to_bytes should have correct signature."""
        sig = inspect.signature(memstr_to_bytes)
        params = list(sig.parameters.keys())
        assert params == ["text"]

    def test_return_type(self) -> None:
        """memstr_to_bytes should return int."""
        result = memstr_to_bytes("100M")
        assert_type(result, int)
        assert isinstance(result, int)


class TestMkdirp:
    """Test mkdirp type hints."""

    def test_exists(self) -> None:
        """mkdirp should exist in runtime."""
        assert hasattr(disk_runtime, "mkdirp")
        assert callable(disk_runtime.mkdirp)

    def test_signature(self) -> None:
        """mkdirp should have correct signature."""
        sig = inspect.signature(mkdirp)
        params = list(sig.parameters.keys())
        assert params == ["d"]

    def test_return_type(self) -> None:
        """mkdirp should return None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_dir"
            mkdirp(test_path)
            # Functions that return None don't need assert_type
            assert test_path.exists()


class TestRmSubdirs:
    """Test rm_subdirs type hints."""

    def test_exists(self) -> None:
        """rm_subdirs should exist in runtime."""
        assert hasattr(disk_runtime, "rm_subdirs")
        assert callable(disk_runtime.rm_subdirs)

    def test_signature(self) -> None:
        """rm_subdirs should have correct signature."""
        sig = inspect.signature(rm_subdirs)
        params = list(sig.parameters.keys())
        assert params == ["path", "onerror"]

    def test_return_type(self) -> None:
        """rm_subdirs should return None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_subdir"
            test_path.mkdir(parents=True)
            rm_subdirs(tmpdir)
            # Functions that return None don't need assert_type
            assert not test_path.exists()


class TestDeleteFolder:
    """Test delete_folder type hints."""

    def test_exists(self) -> None:
        """delete_folder should exist in runtime."""
        assert hasattr(disk_runtime, "delete_folder")
        assert callable(disk_runtime.delete_folder)

    def test_signature(self) -> None:
        """delete_folder should have correct signature."""
        sig = inspect.signature(delete_folder)
        params = list(sig.parameters.keys())
        assert params == ["folder_path", "onerror", "allow_non_empty"]

    def test_return_type(self) -> None:
        """delete_folder should return None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / "test_folder"
            test_path.mkdir(parents=True)
            delete_folder(test_path)
            # Functions that return None don't need assert_type
            assert not test_path.exists()
