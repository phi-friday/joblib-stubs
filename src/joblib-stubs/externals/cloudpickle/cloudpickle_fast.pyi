from typing import Any

from . import cloudpickle as cloudpickle

def __getattr__(name: str) -> Any: ...  # pyright: ignore[reportIncompleteStub]
