---
name: joblib-stub-updater
description: >
  Detects changes between joblib versions by comparing git diffs, analyzes API changes 
  (new/modified/removed functions, classes, parameters), and updates corresponding .pyi stub files.
  Use when joblib releases a new version and stubs need to be synchronized, or when the user 
  mentions "update stubs", "joblib upgrade", "sync stubs with joblib", or "check joblib changes".
license: MIT
compatibility: Requires git, uv, and Python 3.11+. Internet access needed to fetch joblib releases.
allowed-tools: Bash(git:*) Bash(uv:*) Read Write
---

# Joblib Stub Updater

This skill helps maintain type stubs for joblib by detecting API changes between versions and updating `.pyi` files accordingly.

## Workflow Overview

```
1. Detect Version Change  →  2. Generate Diff  →  3. Analyze Changes  →  4. Update Stubs  →  5. Validate
```

## Step 1: Check Current and Latest Versions

First, determine what versions we're working with:

```bash
# Check currently stubbed version (from pyproject.toml or installed)
uv run python -c "import joblib; print(joblib.__version__)"

# Check latest available version from PyPI
curl -s https://pypi.org/pypi/joblib/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])"
```

## Step 2: Clone Joblib and Generate Diff

Clone the joblib repository and generate a diff between versions:

```bash
# Clone joblib to a temp directory (skip if already exists)
if [ ! -d /tmp/joblib-source ]; then
    git clone --depth=100 https://github.com/joblib/joblib.git /tmp/joblib-source
fi

# Navigate to the repository and update tags
cd /tmp/joblib-source
git fetch --tags

# List available tags
git tag --sort=-v:refname | head -20

# Generate diff between two versions (e.g., 1.3.0 to 1.4.0)
git diff <OLD_TAG>..<NEW_TAG> -- joblib/*.py joblib/**/*.py
```

## Step 3: Analyze API Changes

Run the analysis script to identify what changed:

```bash
uv run python skills/joblib-stub-updater/scripts/analyze_changes.py \
    --old-version <OLD_TAG> \
    --new-version <NEW_TAG> \
    --joblib-path /tmp/joblib-source
```

The script will output:
- **New exports**: Functions/classes added to `__all__` or public API
- **Removed exports**: Functions/classes removed from public API  
- **Signature changes**: Parameters added, removed, or type-changed
- **New modules**: Entirely new `.py` files
- **Deprecated items**: Functions/classes marked as deprecated

### Manual Diff Analysis

If the script is unavailable, manually analyze the diff:

```bash
# Navigate to joblib source (assumes Step 2 completed)
cd /tmp/joblib-source

# Focus on public API changes
git diff <OLD_TAG>..<NEW_TAG> -- joblib/__init__.py

# Check specific module changes
git diff <OLD_TAG>..<NEW_TAG> -- joblib/memory.py
git diff <OLD_TAG>..<NEW_TAG> -- joblib/parallel.py

# Look for signature changes (def lines)
git diff <OLD_TAG>..<NEW_TAG> -- 'joblib/*.py' | grep -E '^\+.*def |^\-.*def '
```

## Step 4: Update Stub Files

For each identified change, update the corresponding `.pyi` file:

### Adding New Function

```python
# In src/joblib-stubs/<module>.pyi
def new_function(
    param1: str,
    param2: int = ...,
    *,
    keyword_only: bool = ...,
) -> ReturnType: ...
```

### Adding New Class

```python
class NewClass:
    attr: ClassVar[int]
    
    def __init__(self, param: str) -> None: ...
    def method(self, arg: int) -> str: ...
```

### Modifying Signatures

When a function signature changes:
1. Check the new signature in joblib source
2. Update parameter types and return type
3. Add overloads if the function has multiple valid signatures

```python
@overload
def func(x: int) -> int: ...
@overload  
def func(x: str) -> str: ...
def func(x: int | str) -> int | str: ...
```

### Removing Deprecated Items

If something is removed:
1. Check if it's in stubs
2. Remove from `.pyi` file
3. Remove from `__init__.pyi` re-exports if applicable

## Step 5: Validate Changes

After updating stubs, run full validation:

```bash
cd /path/to/joblib-stubs

# Format and lint
uv run poe lint

# Type check with both checkers
uv run poe pyright
uv run poe mypy

# Run affected tests
uv run pytest src/tests/test_<module>.py -v
```

## Example: Complete Update Flow

### Scenario: Update from joblib 1.3.2 to 1.4.0

```bash
# 1. Setup - Clone joblib repository
if [ ! -d /tmp/joblib-source ]; then
    git clone --depth=100 https://github.com/joblib/joblib.git /tmp/joblib-source
fi
cd /tmp/joblib-source
git fetch --tags

# 2. Generate diff
git diff 1.3.2..1.4.0 -- 'joblib/*.py' > /tmp/joblib-diff.patch

# 3. Review public API changes
git diff 1.3.2..1.4.0 -- joblib/__init__.py
git diff 1.3.2..1.4.0 -- joblib/parallel.py | head -100

# 4. Check new function signatures
git show 1.4.0:joblib/parallel.py | grep -A 20 "def new_function"

# 5. Update stub - Navigate back to stub repository
cd /home/phi/git/python/repo/joblib-stubs
# Edit src/joblib-stubs/parallel.pyi to add new_function

# 6. Validate
uv run poe lint && uv run poe pyright && uv run poe mypy
```

## Change Categories & Actions

| Change Type | Detection | Action |
|-------------|-----------|--------|
| New public function | `+def ` in `__all__` or module | Add to `.pyi` with types |
| New class | `+class ` | Add class stub with methods |
| New parameter | `def func(..., new_param` | Add to stub signature |
| Removed parameter | `-def func(..., old_param` | Remove from stub |
| Type change | Parameter/return type differs | Update type annotation |
| New module | New `.py` file | Create new `.pyi` file |
| Removed function | `-def ` or removed from `__all__` | Remove from stub |
| Deprecated | `@deprecated` or warnings | Add deprecation notice |

## Tips

1. **Always verify runtime behavior first**:
   ```bash
   uv run python -c "import inspect; from joblib import X; print(inspect.signature(X))"
   ```

2. **Check if default values matter for types**:
   ```python
   # If default is None, the type should include None
   def func(param: str | None = ...) -> str: ...
   ```

3. **Handle `*args` and `**kwargs` properly**:
   ```python
   def func(*args: Any, **kwargs: Any) -> Result: ...
   ```

4. **Use `_typeshed.pyi` for complex internal types**

5. **Write tests for new additions** following the patterns in `AGENTS.md`

## Reference Files

- [REFERENCE.md](references/REFERENCE.md) - Detailed stub writing conventions
- [analyze_changes.py](scripts/analyze_changes.py) - Automated change analysis script
