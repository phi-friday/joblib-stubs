import typing

class _Process(typing.Protocol):
    pid: int
    returncode: int | None
    kill: typing.Callable[[], None]
    join: typing.Callable[[], None]

def kill_process_tree(process: _Process, use_psutil: bool = ...) -> None: ...
def recursive_terminate(process: _Process, use_psutil: bool = ...) -> None: ...
def get_exitcodes_terminated_worker(
    processes: typing.Mapping[typing.Any, _Process],
) -> str: ...
