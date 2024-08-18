from typing import Any

from _typeshed import Incomplete
from joblib.disk import mkdirp as mkdirp

def format_time(t: float) -> str: ...
def short_format_time(t: float) -> str: ...
def pformat(obj: Any, indent: int = ..., depth: int = ...) -> str: ...

class Logger:
    depth: Incomplete
    def __init__(self, depth: int = ..., name: str | None = ...) -> None: ...
    def warn(self, msg: Any) -> None: ...
    def info(self, msg: Any) -> None: ...
    def debug(self, msg: Any) -> None: ...
    def format(self, obj: Any, indent: int = ...) -> str: ...

class PrintTime:
    last_time: float
    start_time: float
    logfile: str
    def __init__(self, logfile: str | None = ..., logdir: str | None = ...) -> None: ...
    def __call__(self, msg: str = ..., total: bool = ...) -> None: ...
