from typing import Iterable

def close_fds(keep_fds: Iterable[int]) -> None: ...
def fork_exec(
    cmd: str | bytes | tuple[str | bytes, ...],
    keep_fds: Iterable[int],
    env: dict[str, str] | None = ...,
) -> int | None: ...
