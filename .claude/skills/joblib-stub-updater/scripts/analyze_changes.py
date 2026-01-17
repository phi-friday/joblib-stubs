#!/usr/bin/env -S uv run --script
"""Analyze changes between joblib versions for stub updates.

This script compares two versions of joblib and outputs a structured report
of API changes that need to be reflected in the stub files.

Usage:
    python analyze_changes.py --old-version 1.3.2 --new-version 1.4.0 \
        --joblib-path /tmp/joblib-source

Output:
    - JSON report of changes
    - Human-readable summary
"""
# ruff: noqa: T201, S603, S607

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


@dataclass
class FunctionInfo:
    """Information about a function signature."""

    name: str
    params: list[str]
    defaults: list[str]
    return_annotation: str | None = None
    decorators: list[str] = field(default_factory=list)
    is_async: bool = False

    def signature_str(self) -> str:
        """Return a string representation of the function signature."""
        return f"{self.name}({', '.join(self.params)})"


@dataclass
class ClassInfo:
    """Information about a class."""

    name: str
    bases: list[str]
    methods: dict[str, FunctionInfo]
    class_vars: list[str]


@dataclass
class ModuleInfo:
    """Information about a module's public API."""

    name: str
    functions: dict[str, FunctionInfo]
    classes: dict[str, ClassInfo]
    exports: list[str]  # __all__
    imports: list[str]  # re-exported names


@dataclass
class Change:
    """A single API change."""

    type: str  # 'added', 'removed', 'modified'
    category: str  # 'function', 'class', 'parameter', 'module'
    module: str
    name: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "category": self.category,
            "module": self.module,
            "name": self.name,
            "details": self.details,
        }


def _extract_params(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """Extract parameter list from a function node."""
    params: list[str] = []

    # Regular arguments
    for arg in node.args.args:
        param = arg.arg
        if arg.annotation:
            param += f": {ast.unparse(arg.annotation)}"
        params.append(param)

    # *args
    if node.args.vararg:
        vararg = f"*{node.args.vararg.arg}"
        if node.args.vararg.annotation:
            vararg += f": {ast.unparse(node.args.vararg.annotation)}"
        params.append(vararg)
    elif node.args.kwonlyargs:
        params.append("*")

    # keyword-only arguments
    for arg in node.args.kwonlyargs:
        param = arg.arg
        if arg.annotation:
            param += f": {ast.unparse(arg.annotation)}"
        params.append(param)

    # **kwargs
    if node.args.kwarg:
        kwarg = f"**{node.args.kwarg.arg}"
        if node.args.kwarg.annotation:
            kwarg += f": {ast.unparse(node.args.kwarg.annotation)}"
        params.append(kwarg)

    return params


class ASTVisitor(ast.NodeVisitor):
    """Extract API information from Python AST."""

    def __init__(self) -> None:
        """Initialize the visitor with empty collections."""
        self.functions: dict[str, FunctionInfo] = {}
        self.classes: dict[str, ClassInfo] = {}
        self.exports: list[str] = []
        self.imports: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a function definition node."""
        self._process_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit an async function definition node."""
        self._process_function(node, is_async=True)
        self.generic_visit(node)

    def _process_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, *, is_async: bool = False
    ) -> None:
        """Process a function node and extract its information."""
        if node.name.startswith("_") and not node.name.startswith("__"):
            return  # Skip private functions (but keep dunder methods)

        params = _extract_params(node)
        defaults = [ast.unparse(d) for d in node.args.defaults]
        return_annotation = ast.unparse(node.returns) if node.returns else None
        decorators = [ast.unparse(d) for d in node.decorator_list]

        self.functions[node.name] = FunctionInfo(
            name=node.name,
            params=params,
            defaults=defaults,
            return_annotation=return_annotation,
            decorators=decorators,
            is_async=is_async,
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition node."""
        if node.name.startswith("_"):
            return

        bases = [ast.unparse(b) for b in node.bases]
        methods: dict[str, FunctionInfo] = {}
        class_vars: list[str] = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                func_visitor = ASTVisitor()
                func_visitor._process_function(item)
                if item.name in func_visitor.functions:
                    methods[item.name] = func_visitor.functions[item.name]
            elif isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                class_vars.append(item.target.id)

        self.classes[node.name] = ClassInfo(
            name=node.name, bases=bases, methods=methods, class_vars=class_vars
        )

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit an assignment node to capture __all__."""
        for target in node.targets:
            if (
                isinstance(target, ast.Name)
                and target.id == "__all__"
                and isinstance(node.value, ast.List)
            ):
                self.exports.extend(
                    elt.value
                    for elt in node.value.elts
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit an import-from node to capture re-exports."""
        for alias in node.names:
            name = alias.asname or alias.name
            if not name.startswith("_"):
                self.imports.append(name)
        self.generic_visit(node)


def parse_module(source: str) -> ModuleInfo | None:
    """Parse a Python source file and extract API information."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    visitor = ASTVisitor()
    visitor.visit(tree)

    return ModuleInfo(
        name="",
        functions=visitor.functions,
        classes=visitor.classes,
        exports=visitor.exports,
        imports=visitor.imports,
    )


def get_file_at_version(repo_path: Path, version: str, file_path: str) -> str | None:
    """Get file contents at a specific git tag."""
    try:
        result = subprocess.run(
            ["git", "show", f"{version}:{file_path}"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return None
    else:
        # Try UTF-8 first, fall back to latin-1
        try:
            return result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            return result.stdout.decode("latin-1")


def compare_functions(
    old: dict[str, FunctionInfo], new: dict[str, FunctionInfo], module: str
) -> list[Change]:
    """Compare functions between two versions."""
    changes: list[Change] = []

    old_names = set(old.keys())
    new_names = set(new.keys())

    # Added functions
    changes.extend(
        Change(
            type="added",
            category="function",
            module=module,
            name=name,
            details={
                "signature": new[name].signature_str(),
                "params": new[name].params,
                "return": new[name].return_annotation,
                "decorators": new[name].decorators,
            },
        )
        for name in new_names - old_names
    )

    # Removed functions
    changes.extend(
        Change(type="removed", category="function", module=module, name=name)
        for name in old_names - new_names
    )

    # Modified functions
    for name in old_names & new_names:
        old_func = old[name]
        new_func = new[name]

        if old_func.params != new_func.params:
            changes.append(
                Change(
                    type="modified",
                    category="function",
                    module=module,
                    name=name,
                    details={
                        "old_params": old_func.params,
                        "new_params": new_func.params,
                        "old_signature": old_func.signature_str(),
                        "new_signature": new_func.signature_str(),
                    },
                )
            )
        elif old_func.return_annotation != new_func.return_annotation:
            changes.append(
                Change(
                    type="modified",
                    category="function",
                    module=module,
                    name=name,
                    details={
                        "old_return": old_func.return_annotation,
                        "new_return": new_func.return_annotation,
                    },
                )
            )

    return changes


def compare_classes(
    old: dict[str, ClassInfo], new: dict[str, ClassInfo], module: str
) -> list[Change]:
    """Compare classes between two versions."""
    changes: list[Change] = []

    old_names = set(old.keys())
    new_names = set(new.keys())

    # Added classes
    changes.extend(
        Change(
            type="added",
            category="class",
            module=module,
            name=name,
            details={
                "bases": new[name].bases,
                "methods": list(new[name].methods.keys()),
                "class_vars": new[name].class_vars,
            },
        )
        for name in new_names - old_names
    )

    # Removed classes
    changes.extend(
        Change(type="removed", category="class", module=module, name=name)
        for name in old_names - new_names
    )

    # Modified classes
    for name in old_names & new_names:
        old_cls = old[name]
        new_cls = new[name]

        # Compare methods
        changes.extend(
            compare_functions(old_cls.methods, new_cls.methods, f"{module}.{name}")
        )

        # Compare class variables
        old_vars = set(old_cls.class_vars)
        new_vars = set(new_cls.class_vars)

        changes.extend(
            Change(
                type="added", category="class_var", module=module, name=f"{name}.{v}"
            )
            for v in new_vars - old_vars
        )
        changes.extend(
            Change(
                type="removed", category="class_var", module=module, name=f"{name}.{v}"
            )
            for v in old_vars - new_vars
        )

    return changes


def _analyze_new_module(module_name: str, new_source: str) -> list[Change]:
    """Analyze a newly added module."""
    changes: list[Change] = [
        Change(type="added", category="module", module=module_name, name=module_name)
    ]

    new_info = parse_module(new_source)
    if new_info:
        changes.extend(
            Change(
                type="added",
                category="function",
                module=module_name,
                name=name,
                details={"signature": func.signature_str()},
            )
            for name, func in new_info.functions.items()
        )
        changes.extend(
            Change(type="added", category="class", module=module_name, name=name)
            for name in new_info.classes
        )

    return changes


def _analyze_modified_module(
    module_name: str, old_source: str, new_source: str
) -> list[Change]:
    """Analyze changes in a modified module."""
    old_info = parse_module(old_source)
    new_info = parse_module(new_source)

    if old_info is None or new_info is None:
        return []

    changes: list[Change] = []

    # Compare functions
    changes.extend(
        compare_functions(old_info.functions, new_info.functions, module_name)
    )

    # Compare classes
    changes.extend(compare_classes(old_info.classes, new_info.classes, module_name))

    # Compare __all__
    old_exports = set(old_info.exports)
    new_exports = set(new_info.exports)

    changes.extend(
        Change(type="added", category="export", module=module_name, name=name)
        for name in new_exports - old_exports
    )
    changes.extend(
        Change(type="removed", category="export", module=module_name, name=name)
        for name in old_exports - new_exports
    )

    return changes


def analyze_module_changes(
    repo_path: Path, old_version: str, new_version: str, module_path: str
) -> list[Change]:
    """Analyze changes in a single module."""
    old_source = get_file_at_version(repo_path, old_version, module_path)
    new_source = get_file_at_version(repo_path, new_version, module_path)

    raw_name = module_path.replace("joblib/", "").replace(".py", "").replace("/", ".")
    module_name = "joblib" if raw_name == "__init__" else f"joblib.{raw_name}"

    # Handle new module
    if old_source is None and new_source is not None:
        return _analyze_new_module(module_name, new_source)

    # Handle removed module
    if old_source is not None and new_source is None:
        return [
            Change(
                type="removed", category="module", module=module_name, name=module_name
            )
        ]

    # Handle modified module
    if old_source is None or new_source is None:
        return []

    return _analyze_modified_module(module_name, old_source, new_source)


def get_python_files(repo_path: Path, version: str) -> list[str]:
    """Get list of Python files in joblib at a specific version."""
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", version, "joblib/"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError:
        return []
    else:
        return [f for f in result.stdout.strip().split("\n") if f.endswith(".py")]


def analyze_all_changes(
    repo_path: Path, old_version: str, new_version: str
) -> list[Change]:
    """Analyze all changes between two versions."""
    old_files = set(get_python_files(repo_path, old_version))
    new_files = set(get_python_files(repo_path, new_version))

    all_files = old_files | new_files
    all_changes: list[Change] = []

    for file_path in sorted(all_files):
        # Skip test files and truly internal files (starts with _)
        if "/tests/" in file_path:
            continue
        # Only skip files that start with underscore (like _types.py, _internal.py)
        # but not async_client.py or base_server.py
        file_name = file_path.split("/")[-1]
        if file_name.startswith("_") and file_name != "__init__.py":
            continue

        changes = analyze_module_changes(repo_path, old_version, new_version, file_path)
        all_changes.extend(changes)

    return all_changes


def _format_added_change(change: Change) -> str:
    """Format an added change for the report."""
    if change.category == "module":
        return f"- **New module**: `{change.name}`"
    if change.category == "function":
        sig = change.details.get("signature", change.name)
        return f"- `{change.module}`: function `{sig}`"
    if change.category == "class":
        return f"- `{change.module}`: class `{change.name}`"
    if change.category == "export":
        return f"- `{change.module}`: export `{change.name}`"
    return f"- `{change.module}`: {change.category} `{change.name}`"


def _format_modified_change(change: Change) -> list[str]:
    """Format a modified change for the report."""
    lines = [f"- `{change.module}`: {change.category} `{change.name}`"]
    if "old_signature" in change.details:
        lines.append(f"  - Old: `{change.details['old_signature']}`")
        lines.append(f"  - New: `{change.details['new_signature']}`")
    if "old_return" in change.details:
        old_ret = change.details["old_return"]
        new_ret = change.details["new_return"]
        lines.append(f"  - Return changed: `{old_ret}` → `{new_ret}`")
    return lines


def format_report(changes: list[Change]) -> str:
    """Format changes as a human-readable report."""
    lines = ["# Joblib API Changes Report", ""]

    # Group by type
    added = [c for c in changes if c.type == "added"]
    removed = [c for c in changes if c.type == "removed"]
    modified = [c for c in changes if c.type == "modified"]

    if added:
        lines.extend(["## Added", ""])
        lines.extend(_format_added_change(c) for c in added)
        lines.append("")

    if removed:
        lines.extend(["## Removed", ""])
        lines.extend(f"- `{c.module}`: {c.category} `{c.name}`" for c in removed)
        lines.append("")

    if modified:
        lines.extend(["## Modified", ""])
        for c in modified:
            lines.extend(_format_modified_change(c))
        lines.append("")

    if not changes:
        lines.append("No public API changes detected.")

    return "\n".join(lines)


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Analyze joblib API changes between versions"
    )
    parser.add_argument(
        "--old-version", required=True, help="Old version tag (e.g., 1.3.2)"
    )
    parser.add_argument(
        "--new-version", required=True, help="New version tag (e.g., 1.4.0)"
    )
    parser.add_argument(
        "--joblib-path", required=True, help="Path to joblib git repository"
    )
    parser.add_argument(
        "--output", choices=["json", "text"], default="text", help="Output format"
    )
    parser.add_argument("--output-file", help="Write output to file")

    args = parser.parse_args()
    repo_path = Path(args.joblib_path)

    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)

    print(
        f"Analyzing changes from {args.old_version} to {args.new_version}...",
        file=sys.stderr,
    )

    changes = analyze_all_changes(repo_path, args.old_version, args.new_version)

    if args.output == "json":
        output = json.dumps([c.to_dict() for c in changes], indent=2)
    else:
        output = format_report(changes)

    if args.output_file:
        Path(args.output_file).write_text(output)
        print(f"Output written to {args.output_file}", file=sys.stderr)
    else:
        print(output)

    print(f"\nTotal changes: {len(changes)}", file=sys.stderr)


if __name__ == "__main__":
    main()
