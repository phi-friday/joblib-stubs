from types import ModuleType
from typing import Any, Mapping

WINEXE: bool
WINSERVICE: bool
_python_exe: str

def get_executable() -> str: ...
def get_preparation_data(name: str, init_main_module: bool = ...) -> dict[str, Any]: ...

old_main_modules: list[ModuleType]

def prepare(data: Mapping[str, Any], parent_sentinel: Any = ...) -> None: ...
