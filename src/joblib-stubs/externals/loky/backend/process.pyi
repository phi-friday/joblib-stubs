from _typeshed import Incomplete
from multiprocessing.process import BaseProcess

class LokyProcess(BaseProcess):
    env: Incomplete
    authkey: Incomplete
    init_main_module: Incomplete
    def __init__(self, group: Incomplete | None = None, target: Incomplete | None = None, name: Incomplete | None = None, args=(), kwargs={}, daemon: Incomplete | None = None, init_main_module: bool = False, env: Incomplete | None = None) -> None: ...

class LokyInitMainProcess(LokyProcess):
    def __init__(self, group: Incomplete | None = None, target: Incomplete | None = None, name: Incomplete | None = None, args=(), kwargs={}, daemon: Incomplete | None = None) -> None: ...

class AuthenticationKey(bytes):
    def __reduce__(self): ...
