from multiprocessing.process import BaseProcess
from typing import Any, Callable, Iterable, Literal, Mapping

class LokyProcess(BaseProcess):
    _start_method: Literal["loky"]
    env: dict[str, str]
    authkey: bytes
    init_main_module: bool
    def __init__(
        self,
        group: None = ...,
        target: Callable[..., Any] | None = ...,
        name: str | None = ...,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] = ...,
        daemon: bool | None = ...,
        init_main_module: bool = ...,
        env: dict[str, str] | None = ...,
    ) -> None: ...

class LokyInitMainProcess(LokyProcess):
    _start_method: Literal["loky_init_main"]  # type: ignore[assignment]

    def __init__(
        self,
        group: None = ...,
        target: Callable[..., Any] | None = ...,
        name: str | None = ...,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] = ...,
        daemon: bool | None = ...,
    ) -> None: ...

class AuthenticationKey(bytes):
    def __reduce__(self) -> tuple[AuthenticationKey, tuple[bytes]]: ...
