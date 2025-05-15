import os
import shutil
from pathlib import Path
from typing import List
from uuid import uuid4


def directory_exists(path: Path) -> bool:
    return path.is_dir()

def find_directories(path: Path) -> List[str]:
    return [os.path.join(root, d) for root, dirs, _ in os.walk(path) for d in dirs]

def create_directory(path: Path) -> None:
    return path.mkdir(parents=True, exist_ok=True)

def delete_directory(path: Path) -> None:
    if os.path.isdir(path):
        shutil.rmtree(path)

def delete_directory_contents(path: Path) -> None:
    for item in path.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)

def create_temp_directory() -> Path:
    """
    Generate a temporary directory with a unique id.
    :return: The path to the temporary directory.
    """
    uuid = str(uuid4())
    current_dir = os.getcwd()
    path = Path(current_dir).joinpath('tmp', uuid)
    create_directory(path)
    return path

def create_file(path: Path, name: str, content: List[str] = []) -> None:
    """
    Create a file with the specified name and content.
    :param path: The directory where the file will be created.
    :param name: The name of the file.
    :param content: The content to write to the file.
    """
    with open(path.joinpath(name), 'w') as f:
        for line in content:
            f.write(line + '\n')

def read_file_content(path: Path) -> List[str]:
    """
    Read the content of a file.
    :param path: The path to the file.
    :return: The content of the file as a list of lines.
    """
    if not path.exists():
        return []
    with open(path, 'r') as f:
        return f.readlines()