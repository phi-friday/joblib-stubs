import typing

from _typeshed import StrOrBytesPath
from joblib._memmapping_reducer import WindowsError as WindowsError

def disk_used(path: StrOrBytesPath) -> int: ...
def memstr_to_bytes(text: str) -> int: ...
def mkdirp(d: StrOrBytesPath) -> None: ...

RM_SUBDIRS_RETRY_TIME: float
RM_SUBDIRS_N_RETRY: int

def rm_subdirs(
    path: StrOrBytesPath,
    onerror: typing.Callable[
        [typing.Callable[..., typing.Any], str, typing.Any], object
    ]
    | None = ...,
) -> None: ...
def delete_folder(
    folder_path: StrOrBytesPath,
    onerror: typing.Callable[
        [typing.Callable[..., typing.Any], str, typing.Any], object
    ]
    | None = ...,
    allow_non_empty: bool = ...,
) -> None: ...
