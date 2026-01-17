# Example: Updating Stubs from 1.4.2 to 1.5.0

This document shows a complete example of updating joblib-stubs based on changes detected between versions 1.4.2 and 1.5.0.

## 1. Detect Changes

Run the analysis script:

```bash
cd /path/to/joblib-stubs
uv run python skills/joblib-stub-updater/scripts/analyze_changes.py \
    --old-version 1.4.2 \
    --new-version 1.5.0 \
    --joblib-path /tmp/joblib-source
```

### Key Changes Found:

**Public API (needs stub updates):**
- ✅ New exports: `ParallelBackendBase`, `StoreBackendBase` 
- ✅ `Memory.__init__`: removed `bytes_limit` parameter
- ✅ `numpy_pickle.dump`: removed `cache_size` parameter
- ✅ `numpy_pickle.load`: added `ensure_native_byte_order` parameter
- ✅ `Parallel.__init__`: added `**backend_kwargs`

**Internal (usually skip):**
- Test file changes
- `loky.backend` internals

## 2. Update __init__.pyi

Add new exports to `src/joblib-stubs/__init__.pyi`:

```python
# Before (1.4.2)
from .parallel import Parallel as Parallel

# After (1.5.0) - add new exports
from ._parallel_backends import ParallelBackendBase as ParallelBackendBase
from ._store_backends import StoreBackendBase as StoreBackendBase
from .parallel import Parallel as Parallel
```

## 3. Update memory.pyi

Remove `bytes_limit` parameter from `Memory.__init__`:

```python
# Before (1.4.2)
class Memory:
    def __init__(
        self,
        location: str | os.PathLike[str] | None = ...,
        backend: str = ...,
        mmap_mode: str | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        bytes_limit: int | str | None = ...,  # REMOVE THIS
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...

# After (1.5.0)
class Memory:
    def __init__(
        self,
        location: str | os.PathLike[str] | None = ...,
        backend: str = ...,
        mmap_mode: str | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
```

## 4. Update numpy_pickle.pyi

### Remove `cache_size` from `dump`:

```python
# Before
def dump(
    value: Any,
    filename: str | os.PathLike[str] | IO[bytes],
    compress: bool | int | tuple[str, int] = ...,
    protocol: int | None = ...,
    cache_size: int | None = ...,  # REMOVE
) -> list[str]: ...

# After
def dump(
    value: Any,
    filename: str | os.PathLike[str] | IO[bytes],
    compress: bool | int | tuple[str, int] = ...,
    protocol: int | None = ...,
) -> list[str]: ...
```

### Add `ensure_native_byte_order` to `load`:

```python
# Before
def load(
    filename: str | os.PathLike[str] | IO[bytes],
    mmap_mode: str | None = ...,
) -> Any: ...

# After
def load(
    filename: str | os.PathLike[str] | IO[bytes],
    mmap_mode: str | None = ...,
    ensure_native_byte_order: bool = ...,
) -> Any: ...
```

## 5. Update parallel.pyi

Add `**backend_kwargs` to `Parallel.__init__`:

```python
# After (1.5.0)
class Parallel:
    def __init__(
        self,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase | None = ...,
        return_as: Literal["list", "generator", "generator_unordered"] = ...,
        verbose: int = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | str = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: str | None = ...,
        prefer: Literal["processes", "threads"] | None = ...,
        require: Literal["sharedmem"] | None = ...,
        **backend_kwargs: Any,  # NEW
    ) -> None: ...
```

## 6. Validate

```bash
# Lint and format
uv run poe lint

# Type check
uv run poe pyright
uv run poe mypy

# Run tests
uv run pytest src/tests/ -v
```

## 7. Update Tests

Add tests for new parameters:

```python
# In test_numpy_pickle.py
class TestLoad:
    def test_ensure_native_byte_order_param(self) -> None:
        sig = inspect.signature(mod.load)
        assert "ensure_native_byte_order" in sig.parameters
```

## Summary Checklist

| Module | Change | Status |
|--------|--------|--------|
| `__init__.pyi` | Add `ParallelBackendBase`, `StoreBackendBase` | ☐ |
| `memory.pyi` | Remove `bytes_limit` | ☐ |
| `numpy_pickle.pyi` | Remove `cache_size` from `dump` | ☐ |
| `numpy_pickle.pyi` | Add `ensure_native_byte_order` to `load` | ☐ |
| `parallel.pyi` | Add `**backend_kwargs` | ☐ |
| Tests | Update signature tests | ☐ |
| Validate | `poe lint && poe pyright && poe mypy` | ☐ |
