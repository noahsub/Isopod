import os.path
from pathlib import Path
from subprocess import CompletedProcess
from typing import Tuple, List

from Managers.file_manager import directory_exists, create_directory
from Managers.system_manager import has_permission, run_command


def base_command(location: Path) -> Tuple[List[str], List[Tuple[str, str]]]:
    environment_variables = [
        ('XDG_RUNTIME_DIR', f'{location}/data/xdg'),
    ]
    return (['podman',
             '--root', str(location.joinpath('data', 'storage')),
             '--runroot', str(location.joinpath('data', 'run')),
             '--tmpdir', str(location.joinpath('data', 'tmp')),
             '--storage-opt', 'mount_program=/usr/bin/fuse-overlayfs'],
            environment_variables)

def create_pod(location: Path, name: str, ports: List[Tuple[int, int]] = [], dns='1.1.1.1'):
    # If the directory has not been created yet
    if not directory_exists(location):
        # Check if the parent directory exists and the user has permissions for it
        if not (directory_exists(location.parent) and has_permission(location.parent)):
            # Either the parent directory does not exist or the user does not have permissions, hence return
            return
        else:
            # Create the directory
            create_directory(location)
            create_directory(location.joinpath('data'))
            create_directory(location.joinpath('data', 'storage'))
            create_directory(location.joinpath('data', 'run'))
            create_directory(location.joinpath('data', 'tmp'))
            create_directory(location.joinpath('data', 'xdg'))

    cmd, environment_variables = base_command(location)
    cmd += ['pod', 'create', '--name', name, '--dns', dns]
    for port in ports:
        cmd += ['--publish', f'{port[0]}:{port[1]}']
    return run_command(cmd, capture_output=True, text=True, env=environment_variables)

def list_pods(location: Path) -> CompletedProcess:
    cmd, environment_variables = base_command(location)
    cmd += ['pod', 'ps', '--format', 'json']
    return run_command(cmd, capture_output=True, text=True, env=environment_variables)

def list_containers(location: Path) -> CompletedProcess:
    cmd, environment_variables = base_command(location)
    cmd += ['ps', '--all', '--format', 'json']
    return run_command(cmd, capture_output=True, text=True, env=environment_variables)

def create_container(location: Path,
                     name: str,
                     image: str,
                     env: List[Tuple[str, str]] = [],
                     ports: List[Tuple[int, int]] = [],
                     volumes: List[Tuple[str, str]] = [],
                     command: str = '',
                     detach: bool = True,
                     interactive: bool = True,
                     tty: bool = True,
                     dns: str = '1.1.1.1',
                     pod: str = '') -> CompletedProcess | None:
    """
    Create a podman container.
    :param location: The directory to store the container
    :param name: The name of the container
    :param image: The image to use
    :return:
    """

    # If the directory has not been created yet
    if not directory_exists(location):
        # Check if the parent directory exists and the user has permissions for it
        if not (directory_exists(location.parent) and has_permission(location.parent)):
            # Either the parent directory does not exist or the user does not have permissions, hence return
            return
        else:
            # Create the directory
            create_directory(location)
            create_directory(location.joinpath('data'))
            create_directory(location.joinpath('data', 'storage'))
            create_directory(location.joinpath('data', 'run'))
            create_directory(location.joinpath('data', 'tmp'))
            create_directory(location.joinpath('data', 'xdg'))

    # Check if the user has permissions for the directory
    if not has_permission(location):
        # The user does not have permissions, hence return
        return

    cmd, environment_variables = base_command(location)

    cmd += ['run']

    if detach:
        cmd += ['--detach']
    if interactive:
        cmd += ['--interactive']
    if tty:
        cmd += ['--tty']

    cmd += ['--name', name]

    for e in env:
        cmd += ['--env', f'{e[0]}={e[1]}']

    for port in ports:
        cmd += ['--publish', f'{port[0]}:{port[1]}']

    for volume in volumes:
        cmd += ['--volume', f'{volume[0]}:{volume[1]}']

    cmd += ['--dns', dns]

    if pod:
        cmd += ['--pod', pod]

    cmd += [image]
    cmd += [command]

    result = run_command(cmd, capture_output=True, text=True, env=environment_variables)
    return result






# if __name__ == '__main__':
    # Location
    # location = Path('/containers/podman/alpine3')
    #
    # # Container 1
    # result = create_container(location=location,
    #                           name='alpine3',
    #                           image='alpine',
    #                           command='sh')
    # print(result.returncode, result.stdout, result.stderr)
    #
    # for e in base_command(location)[1]:
    #     print(f'export {e[0]}={e[1]}')
    # print(' '.join(base_command(location)[0]))


