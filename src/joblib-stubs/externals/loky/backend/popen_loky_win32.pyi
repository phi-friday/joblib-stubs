import typing
from multiprocessing import util
from multiprocessing.popen_spawn_win32 import Popen as _Popen  # type: ignore
from multiprocessing.process import BaseProcess

__all__ = ["Popen"]

class Popen(_Popen):  # type: ignore[misc]
    method: typing.Literal["loky"]
    pid: int
    returncode: int | None
    sentinel: int
    finalizer: util.Finalize
    def __init__(self, process_obj: BaseProcess) -> None: ...
