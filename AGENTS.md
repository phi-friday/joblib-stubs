# AGENTS.md

Type stubs for [joblib](https://github.com/joblib/joblib). This repo contains only `.pyi` files, no runtime code.

## Quick Start

```bash
uv sync                    # Install dependencies
uv run poe lint            # Ruff lint + format
uv run poe pyright         # Type check (strict, pyright)
uv run poe mypy            # Type check (strict, mypy)
```

## Project Structure

```
src/
├── joblib-stubs/           # Main stub package
│   ├── __init__.pyi        # Public API re-exports
│   ├── _typeshed.pyi       # Internal type definitions
│   ├── memory.pyi          # Module stubs
│   └── externals/          # Stubs for joblib.externals
└── tests/                  # Stub validation tests
    └── test_<module>.py
```

## Stub Writing Rules

1. Use `...` for function bodies and default values
2. Add type hints to all parameters and return types
3. Use `as` syntax for re-exports: `from mod import X as X`
4. Define internal types in `_typeshed.pyi`
5. Avoid `Incomplete` - use concrete types

```python
def func(param: str, optional: int = ...) -> bool: ...

class Example:
    attr: ClassVar[int]
    def method(self) -> None: ...
```

## Tool Configuration

| Tool | Mode | Notes |
|------|------|-------|
| Mypy | strict | See pyproject.toml for disabled error codes |
| Pyright | strict | See pyrightconfig.json |
| Ruff | ALL | Python 3.11 target |

---

## Test Writing Guide

### Workflow

```bash
# 1. Check runtime behavior first
uv run python -c "import inspect; from joblib.mod import X; print(inspect.signature(X))"

# 2. Write/update stub (.pyi)
# 3. Write tests
# 4. Validate (ALL must pass)
uv run poe lint
uv run poe mypy
uv run poe pyright
uv run pytest src/tests/test_<module>.py -v
```

### Test File Template

```python
"""Tests for joblib.<module> stub types."""

from __future__ import annotations

import inspect
from typing import Any, assert_type

import joblib.<module> as mod
```

**Import Rule**: Use single module alias (`mod`). Only import from other modules when needed for type comparisons.

---

### Testing Classes

```python
class TestClassName:
    """Test ClassName type hints."""

    def test_exists(self) -> None:
        assert hasattr(mod, "ClassName")
        assert inspect.isclass(mod.ClassName)

    def test_inherits(self) -> None:  # if applicable
        assert issubclass(mod.ClassName, mod.ParentClass)

    def test_init_signature(self) -> None:
        sig = inspect.signature(mod.ClassName.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "param1", "param2"]

    def test_attributes(self) -> None:
        obj = mod.ClassName(...)
        assert_type(obj.attr, int)       # stub check FIRST
        assert isinstance(obj.attr, int)  # runtime check SECOND
```

---

### Testing Functions

```python
class TestFunctionName:
    """Test function_name type hints."""

    def test_exists(self) -> None:
        assert hasattr(mod, "function_name")
        assert callable(mod.function_name)

    def test_signature(self) -> None:
        sig = inspect.signature(mod.function_name)
        params = list(sig.parameters.keys())
        assert "param1" in params

    def test_return_type(self) -> None:
        result = mod.function_name(...)
        assert_type(result, ExpectedType)       # stub check FIRST
        assert isinstance(result, ExpectedType)  # runtime check SECOND
```

---

### Testing Type Aliases

Type aliases require both type and identity verification:

```python
class TestTypeAlias:
    """Test TypeAlias assignment."""

    def test_exists(self) -> None:
        assert hasattr(mod, "TypeAlias")

    def test_type(self) -> None:
        assert_type(mod.TypeAlias, type[expected_type])
        assert mod.TypeAlias is expected_type
```

---

### Testing NamedTuples

Custom NamedTuples require thorough field and attribute testing:

```python
class TestCustomNamedTuple:
    """Test CustomNamedTuple type."""

    def test_exists(self) -> None:
        assert hasattr(mod, "CustomNamedTuple")

    def test_is_namedtuple(self) -> None:
        assert hasattr(mod.CustomNamedTuple, "_fields")
        assert issubclass(mod.CustomNamedTuple, tuple)

    def test_fields(self) -> None:
        assert mod.CustomNamedTuple._fields == ("field1", "field2", "field3")

    def test_field1_type(self) -> None:
        instance = mod.CustomNamedTuple(field1=..., field2=..., field3=...)
        assert_type(instance.field1, ExpectedType)
        # Runtime check if applicable

    def test_field2_type(self) -> None:
        instance = mod.CustomNamedTuple(field1=..., field2=..., field3=...)
        assert_type(instance.field2, ExpectedType)
```

---

### Testing Callable Returns

Test both the callable and what it returns:

```python
class TestFactory:
    """Test factory function."""

    def test_exists(self) -> None:
        assert hasattr(mod, "factory")
        assert callable(mod.factory)

    def test_returns_callable(self) -> None:
        result = mod.factory(...)
        assert callable(result)

    def test_returned_callable_result(self) -> None:
        wrapper = mod.factory(...)
        result = wrapper(...)
        assert_type(result, ExpectedType)
        assert isinstance(result, ExpectedType)
```

---

### Key Rules

| Rule | Description |
|------|-------------|
| **assert_type first** | Always before isinstance (narrowing hides errors) |
| **Dual validation** | `assert_type` (stub) + `isinstance` (runtime) for values |
| **Runtime-only** | `hasattr`, `issubclass`, `inspect.isclass` (boolean results) |
| **Single import** | `import joblib.x as mod`, access via `mod.Y` |
| **Test all fields** | NamedTuples: test each field's type individually |

---

### Validation Checklist

All must pass before completion:

```bash
uv run poe lint      # ✓ Ruff lint + format
uv run poe mypy      # ✓ Type check (mypy)
uv run poe pyright   # ✓ Type check (pyright)
uv run pytest src/tests/test_<module>.py -v  # ✓ Tests pass
```

---

## TODO

- Remove `Incomplete` from:
  - `externals/cloudpickle/cloudpickle_fast.pyi`
  - `externals/loky/backend/synchronize.pyi`

## References

- [joblib source](https://github.com/joblib/joblib)
- [PEP 561 - Distributing Type Information](https://peps.python.org/pep-0561/)
