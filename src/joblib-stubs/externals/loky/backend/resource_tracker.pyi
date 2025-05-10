import signal
from collections.abc import Callable, Iterable
from multiprocessing.resource_tracker import ResourceTracker as _ResourceTracker
from typing import Any

from _typeshed import StrOrBytesPath

__all__ = ["ensure_running", "register", "unregister"]

_HAVE_SIGMASK: bool
_IGNORED_SIGNALS: tuple[signal.Signals, signal.Signals]
_CLEANUP_FUNCS: dict[str, Callable[..., Any]]
VERBOSE: bool

class ResourceTracker(_ResourceTracker):
    def __init__(self) -> None: ...
    def maybe_unlink(self, name: str, rtype: str) -> None: ...
    def ensure_running(self) -> None: ...

_resource_tracker: ResourceTracker
ensure_running = _resource_tracker.ensure_running
register = _resource_tracker.register
maybe_unlink = _resource_tracker.maybe_unlink
unregister = _resource_tracker.unregister
getfd = _resource_tracker.getfd

def main(fd: int, verbose: int = ...) -> None: ...
def spawnv_passfds(
    path: StrOrBytesPath, args: tuple[Any, ...], passfds: Iterable[int]
) -> int: ...
