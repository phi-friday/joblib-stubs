import typing

class _ChainedInitializer:
    def __init__(
        self, initializers: typing.Iterable[typing.Callable[..., typing.Any]]
    ) -> None: ...
    def __call__(self, *chained_args: typing.Iterable[typing.Any]) -> None: ...
