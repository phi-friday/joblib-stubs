import typing

def close_fds(keep_fds: typing.Iterable[int]) -> None: ...
def fork_exec(
    cmd: str | bytes | tuple[str | bytes, ...],
    keep_fds: typing.Iterable[int],
    env: dict[str, str] | None = ...,
) -> int | None: ...
