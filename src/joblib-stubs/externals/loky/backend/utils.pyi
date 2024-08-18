from typing import Any, Mapping

from joblib._typeshed import Process

def kill_process_tree(process: Process, use_psutil: bool = ...) -> None: ...
def recursive_terminate(process: Process, use_psutil: bool = ...) -> None: ...
def get_exitcodes_terminated_worker(processes: Mapping[Any, Process]) -> str: ...
