# Example: Updating Stubs from 1.4.2 to 1.5.0

This document shows a complete example of updating joblib-stubs based on actual changes between joblib versions 1.4.2 and 1.5.0.

## 1. Detect Changes

### Setup Repository

```bash
# Clone joblib source if not already present
if [ ! -d /tmp/joblib-source ]; then
    git clone --depth=100 https://github.com/joblib/joblib.git /tmp/joblib-source
fi
cd /tmp/joblib-source
git fetch --tags
```

### Generate Diff

```bash
# View public API changes
git diff 1.4.2..1.5.0 -- joblib/__init__.py

# Check specific module changes
git diff 1.4.2..1.5.0 -- joblib/memory.py | head -100
git diff 1.4.2..1.5.0 -- joblib/numpy_pickle.py | grep -E "def (dump|load)" -A 10
```

### Key Changes Found:

**Public API (needs stub updates):**
- ✅ `__init__.py`: New exports `ParallelBackendBase`, `StoreBackendBase`
- ✅ `Memory.__init__`: removed deprecated `bytes_limit` parameter
- ✅ `numpy_pickle.dump`: removed deprecated `cache_size` parameter

**Internal/formatting (can skip):**
- Import statement reorganization
- Docstring updates
- Code formatting changes

## 2. Update __init__.pyi

Add new exports to `src/joblib-stubs/__init__.pyi`:

```python
# Before (1.4.2) - these classes were not exported
from joblib.parallel import Parallel as Parallel
# ... other imports

# After (1.5.0) - add explicit backend base classes
from joblib._parallel_backends import ParallelBackendBase as ParallelBackendBase
from joblib._store_backends import StoreBackendBase as StoreBackendBase
from joblib.parallel import Parallel as Parallel
# ... other imports

# Also update __all__
__all__ = [
    # ... existing exports
    "ParallelBackendBase",
    "StoreBackendBase",
    # ... other exports
]
```

**Verification:**
```bash
cd /tmp/joblib-source
git diff 1.4.2..1.5.0 -- joblib/__init__.py | grep "ParallelBackendBase\|StoreBackendBase"
```

Output shows these were added to imports in 1.5.0.

## 3. Update memory.pyi

Remove deprecated `bytes_limit` parameter from `Memory.__init__`:

**Verification:**
```bash
cd /tmp/joblib-source

# Check 1.4.2 signature
git show 1.4.2:joblib/memory.py | sed -n '/^class Memory/,/^class /p' | grep "def __init__" -A 5
# Output: def __init__(self, location=None, backend='local',
#                      mmap_mode=None, compress=False, verbose=1, bytes_limit=None,
#                      backend_options=None):

# Check 1.5.0 signature  
git show 1.5.0:joblib/memory.py | sed -n '/^class Memory/,/^class /p' | grep "def __init__" -A 10
# Output: def __init__(
#             self,
#             location=None,
#             backend="local",
#             mmap_mode=None,
#             compress=False,
#             verbose=1,
#             backend_options=None,
#         ):
```

**Stub Update:**
```python
# Necessary imports at top of file (absolute paths)
from pathlib import Path
from typing import Any

from joblib._typeshed import MmapMode
from joblib.logger import Logger

# Before (1.4.2 stub)
class Memory(Logger):
    def __init__(
        self,
        location: str | Path | None = ...,
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        bytes_limit: int | str | None = ...,  # REMOVE THIS LINE
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...

# After (1.5.0 stub)
class Memory(Logger):
    def __init__(
        self,
        location: str | Path | None = ...,
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
```

## 4. Update numpy_pickle.pyi

Remove deprecated `cache_size` parameter from `dump` function:

**Verification:**
```bash
cd /tmp/joblib-source

# Check the diff
git diff 1.4.2..1.5.0 -- joblib/numpy_pickle.py | grep -E "def dump" -A 10

# Output shows:
# -def dump(value, filename, compress=0, protocol=None, cache_size=None):
# +def dump(value, filename, compress=0, protocol=None):
```

**Stub Update:**
```python
# Necessary imports at top of file (absolute paths)
from pathlib import Path
from typing import IO, Any

# Before (1.4.2 stub)
def dump(
    value: Any,
    filename: str | Path | IO[bytes],
    compress: bool | int | tuple[str, int] = ...,
    protocol: int | None = ...,
    cache_size: int | None = ...,  # REMOVE THIS LINE
) -> list[str]: ...

# After (1.5.0 stub)
def dump(
    value: Any,
    filename: str | Path | IO[bytes],
    compress: bool | int | tuple[str, int] = ...,
    protocol: int | None = ...,
) -> list[str]: ...
```

## 5. Validate Changes

After updating all stubs, run full validation:

```bash
# Navigate back to stub repository
cd /home/phi/git/python/repo/joblib-stubs

# Format and lint
uv run poe lint

# Type check with both checkers
uv run poe pyright
uv run poe mypy

# Run affected tests
uv run pytest src/tests/test_memory.py -v
uv run pytest src/tests/test_numpy_pickle.py -v
uv run pytest src/tests/ -v  # All tests
```

## 6. Update Tests

Update signature tests to match new signatures:

```python
# In src/tests/test_memory.py
class TestMemory:
    def test_init_signature(self) -> None:
        sig = inspect.signature(mod.Memory.__init__)
        params = list(sig.parameters.keys())
        # bytes_limit should NOT be in parameters anymore
        assert "bytes_limit" not in params
        assert "backend_options" in params

# In src/tests/test_numpy_pickle.py
class TestDump:
    def test_dump_signature(self) -> None:
        sig = inspect.signature(mod.dump)
        params = list(sig.parameters.keys())
        # cache_size should NOT be in parameters anymore
        assert "cache_size" not in params
        assert params == ["value", "filename", "compress", "protocol"]
```

## Summary Checklist

| Module | Change | Status |
|--------|--------|--------|
| `__init__.pyi` | Add `ParallelBackendBase`, `StoreBackendBase` | ☐ |
| `memory.pyi` | Remove `bytes_limit` from `Memory.__init__` | ☐ |
| `numpy_pickle.pyi` | Remove `cache_size` from `dump` | ☐ |
| Tests | Update signature tests | ☐ |
| Validate | `uv run poe lint && uv run poe pyright && uv run poe mypy` | ☐ |

## Complete Workflow Summary

```bash
# 1. Check versions
uv run python -c "import joblib; print(joblib.__version__)"  # Current: 1.4.2
curl -s https://pypi.org/pypi/joblib/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"  # Latest: 1.5.0

# 2. Clone and analyze
if [ ! -d /tmp/joblib-source ]; then
    git clone --depth=100 https://github.com/joblib/joblib.git /tmp/joblib-source
fi
cd /tmp/joblib-source
git fetch --tags
git diff 1.4.2..1.5.0 -- joblib/__init__.py joblib/memory.py joblib/numpy_pickle.py > /tmp/joblib-1.4.2-to-1.5.0.diff

# 3. Review changes
less /tmp/joblib-1.4.2-to-1.5.0.diff

# 4. Update stubs (manual editing in VS Code)
# - Edit src/joblib-stubs/__init__.pyi
# - Edit src/joblib-stubs/memory.pyi
# - Edit src/joblib-stubs/numpy_pickle.pyi
# - Edit src/tests/test_memory.py
# - Edit src/tests/test_numpy_pickle.py

# 5. Validate
cd /home/phi/git/python/repo/joblib-stubs
uv run poe lint && uv run poe pyright && uv run poe mypy && uv run pytest src/tests/ -v
```
