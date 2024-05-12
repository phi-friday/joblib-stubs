import typing
from multiprocessing.process import BaseProcess

class LokyProcess(BaseProcess):
    _start_method: typing.Literal["loky"]
    env: dict[str, str]
    authkey: bytes
    init_main_module: bool
    def __init__(
        self,
        group: None = ...,
        target: typing.Callable[..., typing.Any] | None = ...,
        name: str | None = ...,
        args: typing.Iterable[typing.Any] = ...,
        kwargs: typing.Mapping[str, typing.Any] = ...,
        daemon: bool | None = ...,
        init_main_module: bool = ...,
        env: dict[str, str] | None = ...,
    ) -> None: ...

class LokyInitMainProcess(LokyProcess):
    _start_method: typing.Literal["loky_init_main"]

    def __init__(
        self,
        group: None = ...,
        target: typing.Callable[..., typing.Any] | None = ...,
        name: str | None = ...,
        args: typing.Iterable[typing.Any] = ...,
        kwargs: typing.Mapping[str, typing.Any] = ...,
        daemon: bool | None = ...,
    ) -> None: ...

class AuthenticationKey(bytes):
    def __reduce__(self) -> tuple[AuthenticationKey, tuple[bytes]]: ...
