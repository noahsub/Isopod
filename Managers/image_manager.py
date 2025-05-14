import json
import pprint
from datetime import datetime, timezone
from typing import List, Dict

import requests

from Managers import log_manager
from Managers.log_manager import LogManager
from Managers.system_manager import run_command


def list_images():
    cmd = ['podman', 'images', '-a', '--format', 'json']
    headers = ['Repository', 'Tag', 'Image ID', 'Created', 'Size']
    data = [headers]
    result = run_command(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        content = json.loads(result.stdout)
        for image in content:
            repository, tag = image['Names'][0].split(':')
            id = image['Id'][:12]
            created = datetime.fromtimestamp(image['Created'], tz=timezone.utc).strftime('%Y-%m-%d')
            size = f'{round(image['Size'] / (1024 ** 2), 2)} MB'
            data.append([repository, tag, id, created, size])
    return data


def fetch_top_docker_hub_images(top_n: int = 25) -> List[List[str]]:
    url = "https://hub.docker.com/v2/repositories/library/"
    response = requests.get(url, params={"page": 1, "page_size": top_n})
    response.raise_for_status()

    data = [['Repository', 'Official', 'Pull Count', 'Star Count', 'Description']]
    for result in response.json().get("results", []):
        data.append([
            result.get('name', 'Unknown'),
            'Yes',  # Official since it's in 'library'
            result.get('pull_count', 0),
            result.get('star_count', 0),
            result.get('description', 'No description available')
        ])

    return data


def search_docker_hub_images(query: str) -> List[List[str]]:
    url = "https://hub.docker.com/v2/search/repositories/"
    response = requests.get(url, params={"query": query})
    response.raise_for_status()

    data = [['Repository', 'Official', 'Pull Count', 'Star Count', 'Description']]
    for result in response.json().get("results", []):
        data.append([
            result.get('repo_name', 'Unknown'),
            'Yes' if result.get('is_official', False) else 'No',
            result.get('pull_count', 0),
            result.get('star_count', 0),
            result.get('short_description', 'No description available')
        ])

    return data


def get_docker_hub_tags(repository: str, max_tags: int = 10) -> List[List[str]]:
    namespace, repo_name = (repository.split('/') if '/' in repository else ('library', repository))
    tags_url = f"https://hub.docker.com/v2/repositories/{namespace}/{repo_name}/tags/"

    response = requests.get(tags_url, params={"page_size": max_tags})
    response.raise_for_status()

    data = [["Repository", "Tag", "Date Created"]]
    for tag in response.json().get("results", []):
        data.append([
            repository,
            tag.get("name", "Unknown"),
            datetime.fromisoformat(tag.get("last_updated", "1970-01-01T00:00:00Z").replace("Z", "+00:00")).strftime(
                "%Y-%m-%d %H:%M:%S UTC")
        ])

    return data


def get_image_url(source: str, repository: str, tag: str = 'latest') -> str:
    namespace, repo_name = (repository.split('/') if '/' in repository else ('library', repository))
    if source == 'docker.io':
        return f'{source}/{namespace}/{repo_name}:{tag}'
    return ''


def pull_image(source: str, repository: str, tag: str = 'latest'):
    url = get_image_url(source, repository, tag)
    log_manager = LogManager()
    log_manager.add_log(f"Attempting to pull {url}...")

    result = run_command(['podman', 'pull', '--quiet', url], capture_output=True, text=True)
    log_manager.add_log(result.stdout)
    log_manager.add_log(result.stderr)
    return result


def remove_image(id: str):
    result = run_command(['podman', 'image', 'rm', id], capture_output=True, text=True)
    log_manager = LogManager()
    log_manager.add_log(f"Attempting to remove {id}...")
    log_manager.add_log(result.stdout)
    log_manager.add_log(result.stderr)
    return result


if __name__ == '__main__':
    # pprint.pprint(search_docker_hub_images('ubuntu/python'))
    pprint.pprint(get_docker_hub_tags('ubuntu/python'))