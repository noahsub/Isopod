import os
import uuid
from pathlib import Path
from git import Repo

from Managers.file_manager import create_directory
from Managers.system_manager import run_command


def clone_github_repository(repo_url: str) -> Path:
    name = repo_url.split('/')[-1].replace('.git', '')
    path = Path(os.getcwd()).joinpath('tmp', 'repositories', f'{uuid.uuid4()}', name)
    create_directory(path)
    Repo.clone_from(repo_url, str(path))
    return Path(path)