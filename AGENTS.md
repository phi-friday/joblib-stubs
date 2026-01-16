# AGENTS.md

Type stubs for [joblib](https://github.com/joblib/joblib). This repo contains only `.pyi` files, no runtime code.

## Quick Start

```bash
uv sync                    # Install dependencies
uv run poe lint            # Ruff lint + format
uv run poe pyright         # Type check (strict, pyright)
uv run poe mypy            # Type check (strict, mypy)
uv run poe check           # Run all checks (pre-commit)
```

## Project Structure

- `src/joblib-stubs/` - Main stub package
  - `__init__.pyi` - Public API re-exports
  - `_typeshed.pyi` - Internal type definitions (TypeAlias, Protocol, TypedDict)
  - `externals/` - Stubs for `joblib.externals` (cloudpickle, loky)
- `typings/joblib/` - Mirror of src for mypy_path

## Stub Writing Rules

1. Use `...` for function bodies and default values
2. Add type hints to all parameters and return types
3. Use `as` syntax for re-exports: `from mod import X as X`
4. Define internal types in `_typeshed.pyi`
5. Avoid `Incomplete` - use concrete types

```python
# Example
def func(param: str, optional: int = ...) -> bool: ...

class Example:
    attr: ClassVar[int]
    def method(self) -> None: ...
```

## Key Settings

| Tool | Mode | Notes |
|------|------|-------|
| Mypy | strict | `disable_error_code`: import-untyped, overload-overlap, override |
| Pyright | strict | See pyrightconfig.json for disabled rules |
| Ruff | ALL | Python 3.11 target |

## Test Writing Principles

### Core Principles

1. **Consistency First**: Apply the same testing pattern to ALL classes/functions in a module
2. **Dual Validation**: Test both runtime behavior AND type checker inference
3. **Runtime-Driven**: Always verify runtime behavior before writing stubs
4. **Full Coverage**: Test exists → inherits → signature → attributes → return types

### Standard Testing Workflow

```bash
# 1. Verify runtime behavior FIRST
uv run python -c "import inspect; from joblib.module import Class; print(inspect.signature(Class.__init__))"

# 2. Write/update stub (.pyi file)
# 3. Write tests following the patterns below
# 4. Run ALL checks - they must ALL pass:

uv run poe lint      # Ruff lint + format
uv run poe mypy      # Mypy type check
uv run poe pyright   # Pyright type check
uv run pytest src/tests/test_module.py -v  # Actual tests

# Or run everything at once:
uv run poe check && uv run pytest src/tests/test_module.py -v
```

### Universal Test Pattern

Every module test file (`src/tests/test_<module>.py`) follows this structure:

```python
"""Tests for joblib.<module> stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.<module> as module_runtime
from joblib.<module> import ClassName, function_name

# For EVERY class, test in this order:
class TestClassName:
    """Test ClassName type hints."""
    
    # 1. Existence (runtime only)
    def test_class_exists(self) -> None:
        """ClassName should exist in runtime."""
        assert hasattr(module_runtime, "ClassName")
        assert inspect.isclass(module_runtime.ClassName)
    
    # 2. Inheritance (runtime only) - if applicable
    def test_inherits(self) -> None:
        """ClassName should inherit from ParentClass."""
        assert issubclass(ClassName, ParentClass)
    
    # 3. Signature (runtime only) - ALWAYS test __init__ for consistency
    def test_init_signature(self) -> None:
        """ClassName.__init__ should have correct signature."""
        sig = inspect.signature(ClassName.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "param1", "param2"]  # or ["self"] if no params
    
    # 4. Attributes (BOTH assert_type + runtime)
    def test_attributes(self) -> None:
        """ClassName attributes should have correct types."""
        obj = ClassName()
        # Type check (what type checker infers)
        assert_type(obj.attr, int)
        # Runtime check (actual value)
        assert isinstance(obj.attr, int)

# For EVERY function, test:
class TestFunctionName:
    """Test function_name type hints."""
    
    # 1. Existence
    def test_exists(self) -> None:
        assert hasattr(module_runtime, "function_name")
        assert callable(module_runtime.function_name)
    
    # 2. Signature
    def test_signature(self) -> None:
        sig = inspect.signature(function_name)
        params = list(sig.parameters.keys())
        assert "param1" in params
        assert "param2" in params
    
    # 3. Return type (BOTH assert_type + runtime)
    def test_return_type(self) -> None:
        result = function_name(...)
        assert_type(result, ExpectedType)
        assert isinstance(result, ExpectedType)
```

### When to Use `assert_type` vs Runtime Checks

**Rule of Thumb**: If it's a **value with a type**, use BOTH. If it's a **boolean check**, use runtime only.

```python
# ✅ Use BOTH (values have types to validate)
assert_type(obj.attr, int)          # Type checker inference
assert isinstance(obj.attr, int)    # Runtime validation

assert_type(func(), str)            # Type checker inference  
assert isinstance(func(), str)      # Runtime validation

# ❌ Runtime ONLY (result is always bool, nothing to type-check)
assert issubclass(Child, Parent)    # Just runtime
assert hasattr(obj, "attr")         # Just runtime
assert inspect.isclass(Foo)         # Just runtime
```

**⚠️ Order Matters**: Always `assert_type` BEFORE `isinstance`/`assert`

```python
# ❌ WRONG ORDER - isinstance narrows the type, hiding stub errors
assert isinstance(obj.attr, int)  # Runtime passes, type gets narrowed to int
assert_type(obj.attr, int)        # Now always passes due to narrowing!
# → Even if stub says obj.attr: str, this will pass!

# ✅ CORRECT ORDER - validates stub first
assert_type(obj.attr, int)        # Catches stub errors (fails if stub says str)
assert isinstance(obj.attr, int)  # Then validates runtime
```

### Consistency Checklist

When writing tests for a module, ensure:

- [ ] **Every** public class has: exists → inherits → init_signature → attributes tests
- [ ] **Every** class with `__init__` has signature test (even if just `["self"]`)
- [ ] **Every** class attribute uses `assert_type` + `isinstance`
- [ ] **Every** function has: exists → signature → return_type tests
- [ ] All tests in the file follow the same pattern and naming
- [ ] Test class names match stub class names: `TestClassName` for `ClassName`

### Validation Checklist (All Must Pass)

```bash
# 1. Linting
uv run poe lint
# or
uv run ruff check src/tests/test_module.py
uv run ruff format src/tests/test_module.py

# 2. Type checking
uv run poe mypy
uv run poe pyright
# or
uv run mypy src/tests/test_module.py
uv run pyright src/tests/test_module.py

# 3. Actual test execution
uv run pytest src/tests/test_module.py -v

# 4. Everything together
uv run poe check
```

**All four must pass with zero errors before considering tests complete.**

## TODO

- Remove all `Incomplete` usage:
  - `externals/cloudpickle/cloudpickle_fast.pyi`
  - `externals/loky/backend/synchronize.pyi`

## References

- [joblib source](https://github.com/joblib/joblib)
- [PEP 561 - Distributing Type Information](https://peps.python.org/pep-0561/)
