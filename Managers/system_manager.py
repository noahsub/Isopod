import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional, Dict, List, Tuple


def run_command(command: List[str], shell=False, capture_output=False, text=False, env: Optional[List[Tuple[str, str]]]=None) -> CompletedProcess:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(dict(env))
    return subprocess.run(command, shell=shell, capture_output=capture_output, text=text, env=merged_env)

def has_permission(path: Path) -> bool:
    read_permission = os.access(path, os.R_OK)
    write_permission = os.access(path, os.W_OK)
    execute_permission = os.access(path, os.X_OK)
    return all((read_permission, write_permission, execute_permission))

def check_selinux(path: Path) -> bool:
    # Check if SELinux is enforced
    result = run_command(['getenforce'], capture_output=True, text=True)
    if result.stdout.strip() != 'Enforcing':
        return False

    # Get SELinux context for the specified directory
    result = run_command(['ls', '-Zd', str(path)], capture_output=True, text=True)
    if result.returncode != 0:
        return False

    parts = result.stdout.strip().split(':')
    if len(parts) < 2:
        return False

    return parts[2] == 'container_file_t'