from collections.abc import Iterable

def fork_exec(
    cmd: str | bytes | tuple[str | bytes, ...],
    keep_fds: Iterable[int],
    env: dict[str, str] | None = ...,
) -> int | None: ...
