from _typeshed import Incomplete

WINEXE: bool
WINSERVICE: bool

def get_executable(): ...
def get_preparation_data(name, init_main_module: bool = True): ...

old_main_modules: Incomplete

def prepare(data, parent_sentinel: Incomplete | None = None) -> None: ...
