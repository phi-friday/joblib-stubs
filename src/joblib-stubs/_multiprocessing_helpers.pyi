from collections.abc import Callable
from types import ModuleType
from typing import Any

mp: ModuleType | None
name: str
assert_spawning: Callable[[Any], None] | None
