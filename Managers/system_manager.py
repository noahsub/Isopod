import os
import shlex
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional, Dict, List, Tuple


def run_command(command: List[str], shell=False, capture_output=False, text=False, env: Optional[List[Tuple[str, str]]]=None) -> CompletedProcess:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(dict(env))

    return subprocess.run(command, shell=shell, capture_output=capture_output, text=text, env=merged_env)

def run_command_interactive(command: List[str], env: Optional[List[Tuple[str, str]]] = None) -> None:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(dict(env))

    subprocess.run(' '.join(shlex.quote(arg) for arg in command), shell=True, env=merged_env)
    return None


def has_permission(path: Path) -> bool:
    read_permission = os.access(path, os.R_OK)
    write_permission = os.access(path, os.W_OK)
    execute_permission = os.access(path, os.X_OK)
    return all((read_permission, write_permission, execute_permission))