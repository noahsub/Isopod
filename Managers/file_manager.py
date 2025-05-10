import os
import shutil
from pathlib import Path
from typing import List


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