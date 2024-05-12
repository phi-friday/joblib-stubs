import types
import typing

WINEXE: bool
WINSERVICE: bool
_python_exe: str

def get_executable() -> str: ...
def get_preparation_data(
    name: str, init_main_module: bool = ...
) -> dict[str, typing.Any]: ...

old_main_modules: list[types.ModuleType]

def prepare(
    data: typing.Mapping[str, typing.Any], parent_sentinel: typing.Any = ...
) -> None: ...
