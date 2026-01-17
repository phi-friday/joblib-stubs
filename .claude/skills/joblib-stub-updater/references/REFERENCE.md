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
# Re-export with explicit `as` syntax
from .module import (
    PublicClass as PublicClass,
    public_function as public_function,
)

# Define __all__ if the source does
__all__ = ["PublicClass", "public_function"]
```

### Internal Types (`_typeshed.pyi`)

Put complex internal types here:

```python
from typing import Protocol, TypeAlias
from collections.abc import Callable

# Type aliases
HashFunc: TypeAlias = Callable[[bytes], bytes]

# Protocols for duck typing
class Hasher(Protocol):
    def update(self, data: bytes) -> None: ...
    def digest(self) -> bytes: ...
```

## Joblib-Specific Patterns

### Memory/Caching

```python
class Memory:
    def __init__(
        self,
        location: str | os.PathLike[str] | None = ...,
        backend: str = ...,
        cachedir: str | os.PathLike[str] | None = ...,  # deprecated
        mmap_mode: str | None = ...,
        compress: bool | int = ...,
        verbose: int = ...,
        bytes_limit: int | str | None = ...,
        backend_options: dict[str, Any] | None = ...,
    ) -> None: ...
    
    def cache(
        self,
        func: Callable[P, T] | None = ...,
        ignore: list[str] | None = ...,
        verbose: int | None = ...,
        mmap_mode: str | None = ...,
        cache_validation_callback: Callable[..., bool] | None = ...,
    ) -> MemorizedFunc[P, T] | Callable[[Callable[P, T]], MemorizedFunc[P, T]]: ...
```

### Parallel Processing

```python
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
    ) -> None: ...
    
    def __call__(self, iterable: Iterable[tuple[Callable[..., T], tuple[Any, ...], dict[str, Any]]]) -> list[T]: ...
```

### `delayed` Function

```python
@overload
def delayed(function: Callable[P, T]) -> Callable[P, tuple[Callable[P, T], tuple[Any, ...], dict[str, Any]]]: ...
@overload
def delayed(function: None = ...) -> Callable[[Callable[P, T]], Callable[P, tuple[Callable[P, T], tuple[Any, ...], dict[str, Any]]]]: ...
```

## Common Type Imports

```python
from __future__ import annotations

import os
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
    TypeVar,
    overload,
)
from collections.abc import (
    Callable,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    Sequence,
)
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
