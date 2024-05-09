from _typeshed import Incomplete
from multiprocessing.popen_spawn_win32 import Popen as _Popen

__all__ = ['Popen']

class Popen(_Popen):
    method: str
    pid: Incomplete
    returncode: Incomplete
    sentinel: Incomplete
    finalizer: Incomplete
    def __init__(self, process_obj) -> None: ...
