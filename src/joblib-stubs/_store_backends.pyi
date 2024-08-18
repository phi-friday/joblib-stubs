from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Callable, Mapping, NamedTuple

from joblib import numpy_pickle as numpy_pickle
from joblib._typeshed import ItemInfo, MmapMode
from joblib.backports import concurrency_safe_rename as concurrency_safe_rename
from joblib.disk import memstr_to_bytes as memstr_to_bytes
from joblib.disk import mkdirp as mkdirp
from joblib.disk import rm_subdirs as rm_subdirs
from joblib.logger import format_time as format_time
from typing_extensions import TypeVar

_T = TypeVar("_T")

class CacheItemInfo(NamedTuple):
    path: str
    size: int
    last_access: datetime

class CacheWarning(Warning): ...

def concurrency_safe_write(
    object_to_write: _T, filename: str, write_func: Callable[[_T, str], Any]
) -> str: ...

class StoreBackendBase(metaclass=ABCMeta):
    location: str
    @abstractmethod
    def create_location(self, location: str) -> None: ...
    @abstractmethod
    def clear_location(self, location: str) -> None: ...
    @abstractmethod
    def get_items(self) -> list[CacheItemInfo]: ...
    @abstractmethod
    def configure(
        self,
        location: str,
        verbose: int = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...

class StoreBackendMixin:
    def load_item(
        self,
        call_id: tuple[str, ...],
        verbose: int = ...,
        timestamp: float | None = ...,
        metadata: Mapping[str, Any] | None = ...,
    ) -> Any: ...
    def dump_item(
        self, call_id: tuple[str, ...], item: Any, verbose: int = ...
    ) -> None: ...
    def clear_item(self, call_id: tuple[str, ...]) -> None: ...
    def contains_item(self, call_id: tuple[str, ...]) -> bool: ...
    def get_item_info(self, call_id: tuple[str, ...]) -> ItemInfo: ...
    def get_metadata(self, call_id: tuple[str, ...]) -> dict[str, Any]: ...
    def store_metadata(
        self, call_id: tuple[str, ...], metadata: dict[str, Any]
    ) -> None: ...
    def contains_path(self, call_id: tuple[str, ...]) -> bool: ...
    def clear_path(self, call_id: tuple[str, ...]) -> None: ...
    def store_cached_func_code(
        self, call_id: tuple[str, ...], func_code: str | None = ...
    ) -> None: ...
    def get_cached_func_code(self, call_id: tuple[str, ...]) -> str: ...
    def get_cached_func_info(self, call_id: tuple[str, ...]) -> ItemInfo: ...
    def clear(self) -> None: ...
    def enforce_store_limits(
        self,
        bytes_limit: int | str | None,
        items_limit: int | None = ...,
        age_limit: timedelta | None = ...,
    ) -> None: ...

class FileSystemStoreBackend(StoreBackendBase, StoreBackendMixin):
    compress: bool
    mmap_mode: MmapMode
    verbose: int
    # mypy
    def create_location(self, location: str) -> None: ...
    def clear_location(self, location: str) -> None: ...
    def get_items(self) -> list[CacheItemInfo]: ...
    def configure(
        self,
        location: str,
        verbose: int = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
