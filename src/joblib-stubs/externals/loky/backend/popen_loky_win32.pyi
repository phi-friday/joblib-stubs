from multiprocessing import util
from multiprocessing.process import BaseProcess
from typing import Literal

# isort: off
from multiprocessing.popen_spawn_win32 import Popen as _Popen  # type: ignore[attr-defined]
# isort: on

__all__ = ["Popen"]

class Popen(_Popen):  # type: ignore[misc]
    method: Literal["loky"]
    pid: int
    returncode: int | None
    sentinel: int
    finalizer: util.Finalize
    def __init__(self, process_obj: BaseProcess) -> None: ...
