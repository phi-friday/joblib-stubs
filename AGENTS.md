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
```

### Universal Test Pattern

Every module test file (`src/tests/test_<module>.py`) follows this structure:

```python
"""Tests for joblib.<module> stub types."""

from __future__ import annotations

import inspect
from typing import assert_type

import joblib.<module> as mod

# ⚠️ IMPORTANT: Use ONLY the module alias for all access
# ❌ WRONG: from joblib.<module> import ClassName, function_name
# ✅ CORRECT: Access via mod.ClassName, mod.function_name

# For EVERY class, test in this order:
class TestClassName:
    """Test ClassName type hints."""
    
    # 1. Existence (runtime only)
    def test_class_exists(self) -> None:
        """ClassName should exist in runtime."""
        assert hasattr(mod, "ClassName")
        assert inspect.isclass(mod.ClassName)
    
    # 2. Inheritance (runtime only) - if applicable
    def test_inherits(self) -> None:
        """ClassName should inherit from ParentClass."""
        assert issubclass(mod.ClassName, mod.ParentClass)
    
    # 3. Signature (runtime only) - ALWAYS test __init__ for consistency
    def test_init_signature(self) -> None:
        """ClassName.__init__ should have correct signature."""
        sig = inspect.signature(mod.ClassName.__init__)
        params = list(sig.parameters.keys())
        assert params == ["self", "param1", "param2"]  # or ["self"] if no params
    
    # 4. Attributes (BOTH assert_type + runtime)
    def test_attributes(self) -> None:
        """ClassName attributes should have correct types."""
        obj = mod.ClassName()
        # Type check (what type checker infers)
        assert_type(obj.attr, int)
        # Runtime check (actual value)
        assert isinstance(obj.attr, int)

# For EVERY function, test:
class TestFunctionName:
    """Test function_name type hints."""
    
    # 1. Existence
    def test_exists(self) -> None:
        assert hasattr(mod, "function_name")
        assert callable(mod.function_name)
    
    # 2. Signature
    def test_signature(self) -> None:
        sig = inspect.signature(mod.function_name)
        params = list(sig.parameters.keys())
        assert "param1" in params
        assert "param2" in params
    
    # 3. Return type (BOTH assert_type + runtime)
    def test_return_type(self) -> None:
        result = mod.function_name(...)
        assert_type(result, ExpectedType)
        assert isinstance(result, ExpectedType)
```

### Import Rules

**Single Module Alias Only**: Import the module once with an alias, then access everything through it.

```python
# ✅ CORRECT - Single import, use module alias everywhere
import joblib.memory as mod

def test_class_exists(self) -> None:
    assert hasattr(mod, "Memory")
    assert inspect.isclass(mod.Memory)

def test_instantiation(self) -> None:
    obj = mod.Memory("/tmp")
    assert_type(obj, mod.Memory)

# ❌ WRONG - Redundant imports
import joblib.memory as memory_runtime
from joblib.memory import Memory, MemorizedFunc  # Redundant!
```

**Exception**: When importing from a DIFFERENT module (e.g., parent class for inheritance check):

```python
import joblib.memory as mod
from joblib.logger import Logger  # OK - different module for inheritance check

def test_inherits(self) -> None:
    assert issubclass(mod.Memory, Logger)
```

### Callable Objects and Return Types

**Always test return types of callable objects**: If a class or function returns a callable object (like `delayed`, factory functions), test both the callable itself AND its return value type.

```python
# For factory functions / decorators that return callables:
class TestDelayed:
    """Test delayed function type hints."""
    
    def test_exists(self) -> None:
        assert hasattr(mod, "delayed")
        assert callable(mod.delayed)
    
    def test_return_type(self) -> None:
        """delayed should return a callable that produces BatchedCall."""
        def sample_func(x: int) -> int:
            return x * 2
        
        # Test the wrapper is callable
        wrapper = mod.delayed(sample_func)
        assert callable(wrapper)
        
        # Test the wrapper's return type when called
        result = wrapper(42)
        assert_type(result, mod.BatchedCall[..., int])  # or appropriate type
        assert isinstance(result, tuple)  # BatchedCall is typically a tuple

# For callable classes (classes with __call__):
class TestBatchedCalls:
    """Test BatchedCalls type hints."""
    
    def test_call_return_type(self) -> None:
        """BatchedCalls.__call__ should return list[Any]."""
        obj = mod.BatchedCalls([], backend)
        result = obj()
        assert_type(result, list[Any])
        assert isinstance(result, list)
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

- [ ] **Single import**: Use `import joblib.<module> as mod`, access all via `mod.X`
- [ ] **No redundant imports**: Do NOT also `from joblib.<module> import X`
- [ ] **Every** public class has: exists → inherits → init_signature → attributes tests
- [ ] **Every** class with `__init__` has signature test (even if just `["self"]`)
- [ ] **Every** class attribute uses `assert_type` + `isinstance`
- [ ] **Every** function has: exists → signature → return_type tests
- [ ] **Every** callable's return type is tested (factories, decorators, `__call__` methods)
- [ ] All tests in the file follow the same pattern and naming
- [ ] Test class names match stub class names: `TestClassName` for `ClassName`

### Validation Checklist (All Must Pass)

```bash
# 1. Linting
uv run poe lint

# 2. Type checking
uv run poe mypy
uv run poe pyright

# 3. Actual test execution
uv run pytest src/tests/test_module.py -v
```

**All three (lint, mypy, pyright, pytest) must pass with zero errors before considering tests complete.**

⚠️ **Do NOT use `uv run poe check`** - it may not accurately reflect individual tool results. Always run `lint`, `mypy`, and `pyright` separately.

## TODO

- Remove all `Incomplete` usage:
  - `externals/cloudpickle/cloudpickle_fast.pyi`
  - `externals/loky/backend/synchronize.pyi`

## References

- [joblib source](https://github.com/joblib/joblib)
- [PEP 561 - Distributing Type Information](https://peps.python.org/pep-0561/)
