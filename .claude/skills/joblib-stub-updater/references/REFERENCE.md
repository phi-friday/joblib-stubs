# Stub Writing Reference

Detailed conventions for writing and maintaining joblib type stubs.

## Type Annotation Patterns

### Basic Patterns

```python
# Simple function
def func(param: str, count: int = ...) -> bool: ...

# Optional parameter (default is None)
def func(param: str | None = ...) -> str: ...

# With *args and **kwargs
def func(*args: Any, **kwargs: Any) -> Result: ...

# Keyword-only parameters
def func(pos_arg: int, *, keyword_only: str = ...) -> None: ...

# Positional-only parameters (Python 3.8+)
def func(pos_only: int, /, normal: str) -> None: ...
```

### Class Patterns

```python
from typing import ClassVar, Self

class MyClass:
    # Class variable
    class_attr: ClassVar[int]
    
    # Instance variable (declared without assignment)
    instance_attr: str
    
    def __init__(self, value: str) -> None: ...
    
    # Method returning same type
    def copy(self) -> Self: ...
    
    # Property
    @property
    def computed(self) -> int: ...
    
    # Setter
    @computed.setter
    def computed(self, value: int) -> None: ...
```

### Overloads

Use `@overload` when a function's return type depends on input types:

```python
from typing import overload

@overload
def process(data: str) -> str: ...
@overload
def process(data: bytes) -> bytes: ...
@overload
def process(data: list[int]) -> list[int]: ...
def process(data: str | bytes | list[int]) -> str | bytes | list[int]: ...
```

### Generic Types

```python
from typing import TypeVar, Generic
from collections.abc import Callable, Iterator

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)

class Container(Generic[T]):
    def get(self) -> T: ...
    def set(self, value: T) -> None: ...

# Callable types
def apply(func: Callable[[int, str], bool], x: int, y: str) -> bool: ...

# With ParamSpec for decorators
from typing import ParamSpec, Concatenate

P = ParamSpec("P")

def decorator(func: Callable[P, T]) -> Callable[P, T]: ...
```

## Module Organization

### `__init__.pyi` Pattern

```python
# Use absolute imports (not relative)
# Re-export with explicit `as` syntax
from joblib.module import (
    PublicClass as PublicClass,
    public_function as public_function,
)

# Define __all__ if the source does
__all__ = ["PublicClass", "public_function"]
```

**Real Example from `__init__.pyi`:**
```python
from joblib._cloudpickle_wrapper import (
    wrap_non_picklable_objects as wrap_non_picklable_objects,
)
from joblib._parallel_backends import ParallelBackendBase
from joblib._store_backends import StoreBackendBase
from joblib.memory import Memory, MemorizedResult, expires_after
from joblib.parallel import Parallel, delayed, cpu_count

__all__ = [
    "Memory",
    "MemorizedResult",
    "Parallel",
    "ParallelBackendBase",
    "cpu_count",
    "delayed",
    "expires_after",
    # ... more exports
]
```

### Internal Types (`_typeshed.pyi`)

Put complex internal types here. Other modules import from this using absolute paths:

```python
# In src/joblib-stubs/_typeshed.pyi
from typing import Protocol, TypeAlias
from collections.abc import Callable

# Type aliases
HashFunc: TypeAlias = Callable[[bytes], bytes]
MmapMode: TypeAlias = str | None

# Protocols for duck typing
class Hasher(Protocol):
    def update(self, data: bytes) -> None: ...
    def digest(self) -> bytes: ...
```

**Usage in other modules:**
```python
# In src/joblib-stubs/memory.pyi
from joblib._typeshed import HashFunc, MmapMode  # Absolute import

def func(hasher: HashFunc, mmap_mode: MmapMode) -> None: ...
```

## Joblib-Specific Patterns

### Memory/Caching

```python
# Necessary imports (absolute paths)
from collections.abc import Awaitable, Callable
from datetime import timedelta
from pathlib import Path
from typing import Any, Generic, overload

from joblib._typeshed import MemoryCacheFunc, MmapMode
from joblib.logger import Logger
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

class Memory(Logger):
    mmap_mode: MmapMode
    verbose: int
    timestamp: float
    backend: str
    compress: bool | int
    backend_options: dict[str, Any]
    location: str | Path
    
    def __init__(
        self,
        location: str | Path | None = ...,
        backend: str = ...,
        mmap_mode: MmapMode | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
    
    # Decorator pattern with overloads
    @overload
    def cache(
        self,
        func: None = ...,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemoryCacheFunc: ...
    @overload
    def cache(
        self,
        func: Callable[_P, Awaitable[_T]],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> AsyncMemorizedFunc[_P, _T]: ...
    @overload
    def cache(
        self,
        func: Callable[_P, _T],
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: MmapMode | bool = ...,
        cache_validation_callback: Callable[..., Any] | None = ...,
    ) -> MemorizedFunc[_P, _T]: ...
    
    def clear(self, warn: bool = ...) -> None: ...
    def reduce_size(
        self,
        bytes_limit: int | str | None = ...,
        items_limit: int | None = ...,
        age_limit: timedelta | None = ...,
    ) -> None: ...
```

### Parallel Processing

```python
# Necessary imports (absolute paths)
from collections.abc import Callable, Iterable
from typing import Any, Generic, Literal, overload

from joblib._parallel_backends import ParallelBackendBase
from joblib._typeshed import (
    MmapMode,
    Prefer,
    Require,
    ReturnAs,
    ReturnList,
    ReturnGererator,
)
from joblib.logger import Logger

class Parallel(Logger, Generic[ReturnAs]):
    # Use overloads for different return types
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnList] | None = ...,
        return_as: Literal["list"] = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnList]: ...
    @overload
    def __new__(
        cls,
        n_jobs: int | None = ...,
        backend: str | ParallelBackendBase[ReturnGererator] | None = ...,
        return_as: Literal["generator"] = ...,
        verbose: int | None = ...,
        timeout: float | None = ...,
        pre_dispatch: int | str = ...,
        batch_size: int | Literal["auto"] = ...,
        temp_folder: str | None = ...,
        max_nbytes: int | str | None = ...,
        mmap_mode: MmapMode | None = ...,
        prefer: Prefer | None = ...,
        require: Require | None = ...,
    ) -> Parallel[ReturnGererator]: ...
    
    # The actual __call__ signature is complex - see parallel.pyi
    def __call__(self, iterable: Iterable[Any]) -> Any: ...
```

### `delayed` Function

```python
# Necessary imports (absolute paths)
from collections.abc import Callable
from joblib._typeshed import BatchedCall
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")

# Simple single signature in actual stubs
def delayed(function: Callable[_P, _T]) -> Callable[_P, BatchedCall[_P, _T]]: ...
```

**Note**: The actual implementation is simpler than you might expect. `BatchedCall` is defined in `_typeshed.pyi` to represent the delayed call tuple structure.

## Common Type Imports

```python
# Standard imports
from __future__ import annotations

import os
from collections.abc import (
    Awaitable,
    Callable,
    Coroutine,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Sequence,
)
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Final,
    Generic,
    Literal,
    NamedTuple,
    Protocol,
    Self,
    TypeAlias,
    overload,
)

# Use typing_extensions for ParamSpec, TypeVar (for compatibility)
from typing_extensions import ParamSpec, TypeVar

# Absolute imports from joblib modules
from joblib._typeshed import CustomType  # Internal types
from joblib.module import SomeClass
```

**Real Example from `memory.pyi`:**
```python
from collections.abc import Awaitable, Callable, Coroutine
from datetime import timedelta
from pathlib import Path
from typing import Any, Generic, overload

from joblib import hashing as hashing
from joblib._store_backends import StoreBackendBase
from joblib._typeshed import MemoryCacheFunc, MmapMode
from joblib.func_inspect import filter_args, format_call
from joblib.logger import Logger
from typing_extensions import ParamSpec, TypeVar

_T = TypeVar("_T")
_P = ParamSpec("_P")
```

## Deprecation Handling

When something is deprecated but still present:

```python
from typing import deprecated
from warnings import deprecated  # Python 3.13+

@deprecated("Use new_function instead")
def old_function(x: int) -> int: ...
```

Or with a comment:

```python
# Deprecated since 1.4.0, use new_function instead
def old_function(x: int) -> int: ...
```

## Mapping Source to Stub

### Source Code
```python
def process_data(data, *, normalize=True, fill_value=0):
    """Process input data.
    
    Parameters
    ----------
    data : array-like
        Input data
    normalize : bool, default=True
        Whether to normalize
    fill_value : int or float, default=0
        Value for missing data
    """
    if normalize:
        data = data / data.max()
    return data
```

### Corresponding Stub
```python
from numpy.typing import ArrayLike, NDArray

def process_data(
    data: ArrayLike,
    *,
    normalize: bool = ...,
    fill_value: int | float = ...,
) -> NDArray[Any]: ...
```

## Testing Checklist

After updating stubs:

1. [ ] `uv run poe lint` - passes
2. [ ] `uv run poe pyright` - passes
3. [ ] `uv run poe mypy` - passes
4. [ ] Tests added/updated for new APIs
5. [ ] `assert_type` checks match runtime behavior
