from pathlib import Path
import shlex

from Managers.file_manager import create_directory, delete_directory, directory_exists
from Managers.system_manager import has_permission, run_command, run_command_interactive

if __name__ == "__main__":
    location = Path(input('Container Directory: '))

    # If the directory has not been created yet
    if not directory_exists(location):
        # Check if the parent directory exists and the user has permissions for it
        if not (directory_exists(location.parent) and has_permission(location.parent)):
            # Either the parent directory does not exist or the user does not have permissions, hence return
            print(f"Either the parent directory does not exist or the user does not have permissions for {location.parent}")
            exit(1)
        else:
            # Create the directory
            create_directory(location)
            create_directory(location.joinpath('data'))
            create_directory(location.joinpath('data', 'storage'))
            create_directory(location.joinpath('data', 'run'))
            # create_directory(location.joinpath('data', 'tmp'))
            # create_directory(location.joinpath('data', 'xdg'))

    # environment_variables = [('XDG_RUNTIME_DIR', str(location.joinpath('data', 'xdg')))]
    environment_variables = []

    podman_base_command = [
        'podman', 
        '--root', str(location.joinpath('data', 'storage')), 
        '--runroot', str(location.joinpath('data', 'run')),
        # '--tmpdir', str(location.joinpath('data', 'tmp')),
        # '--storage-opt', 'mount_program=/usr/bin/fuse-overlayfs'
    ]

    # Check for reboot or errors
    if run_command(podman_base_command + ['ps', '-a'], capture_output=False, text=False).returncode != 0:
        print('Error detected, cleaning up...')
        delete_directory(location.joinpath('data', 'run'))
        # delete_directory(location.joinpath('data', 'tmp'))
        # delete_directory(location.joinpath('data', 'xdg', 'libpod', 'tmp'))
    
    while True:
        # Get input
        command = input('Podman Command (without podman): ')

        # Split the command safely
        cmd = podman_base_command + shlex.split(command)

        # for i in range(len(cmd)):
        #     print(f'[{i}]: {cmd[i]}')

        k = len(podman_base_command)
        if cmd[k] in ['exec', 'attach']:
            run_command_interactive(cmd, environment_variables)

        else:
            output = run_command(cmd, capture_output=True, text=True, env=environment_variables)
            print(f'Return Code: {output.returncode}')
            print(f'Ouput:')
            print(output.stdout)
            print(f'Error:')
            print(output.stderr)
