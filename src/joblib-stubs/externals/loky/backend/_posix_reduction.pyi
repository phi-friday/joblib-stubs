from multiprocessing import resource_sharer
from multiprocessing.connection import Connection
from typing import Callable

from joblib.externals.loky.backend.reduction import register as register

HAVE_SEND_HANDLE: bool

def DupFd(fd: int) -> resource_sharer.DupFd: ...  # noqa: N802
def rebuild_connection(
    df: resource_sharer.DupFd, readable: bool, writable: bool
) -> Connection: ...
def reduce_connection(
    conn: Connection,
) -> tuple[
    Callable[[resource_sharer.DupFd, bool, bool], Connection],
    tuple[resource_sharer.DupFd, bool, bool],
]: ...
