# AGENTS.md

Type stubs for [joblib](https://github.com/joblib/joblib). This repo contains only `.pyi` files, no runtime code.

## Quick Start

```bash
uv sync                    # Install dependencies
uv run poe lint            # Ruff lint + format
uv run poe mypy            # Type check (strict)
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

## TODO

- Remove all `Incomplete` usage:
  - `externals/cloudpickle/cloudpickle_fast.pyi`
  - `externals/loky/backend/synchronize.pyi`

## References

- [joblib source](https://github.com/joblib/joblib)
- [PEP 561 - Distributing Type Information](https://peps.python.org/pep-0561/)
