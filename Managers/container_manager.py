import json
from typing import Optional, List, Dict, Tuple

from Managers.log_manager import LogManager
from Managers.system_manager import run_command

def create_container(name: str, image: str, network: Optional[str] = None, pod: Optional[str] = None, volume: Optional[str] = None, mount_path: Optional[str] = None, command: Optional[str] = None, detached: bool = True, interactive: bool = True, tty: bool = True, ports: Optional[List[Tuple[str, str]]] = None, env_vars: Optional[List[Tuple[str, str]]] = None):

    network = None if network and pod else network

    cmd = ["podman", "run", "--name", name]

    cmd += ["--network", network] if network else []
    cmd += ["--pod", pod] if pod else []
    cmd += ["-v", f"{volume}:{mount_path}"] if volume and mount_path else []

    cmd += [item for host_port, container_port in ports for item in ("-p", f"{host_port}:{container_port}")] if ports else []

    cmd += [item for key, value in env_vars for item in ("--env", f"{key}={value}")] if env_vars else []

    cmd += ["-d"] if detached else []
    cmd += ["-i"] if interactive else []
    cmd += ["-t"] if tty else []

    cmd.append(image)

    cmd.append(command) if command else None

    print(' '.join(cmd))

    # result = run_command(cmd)
    #
    # log_manager = LogManager()
    # log_manager.write_system_log(result)
    #
    # return result


def list_containers() -> List[List[str]]:
    """
    List all podman containers with their details.
    :return: A list of containers with their details.
    """
    cmd = ["podman", "ps", "-a", "--format", "json"]

    headers = ["CONTAINER ID", "IMAGE", "COMMAND", "CREATED", "STATUS", "PORTS", "NAMES"]
    data = [headers]

    result = run_command(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        content = json.loads(result.stdout)
        for container in content:
            container_id = container.get("Id")[:12]  # Shortened ID
            image = container.get("Image")
            command = ' '.join(container.get("Command", [])) if container.get("Command") else ""
            created = container.get("CreatedAt") or ""
            status = container.get("Status") or ""
            ports = ', '.join([f"{p['HostPort']}/{p['Protocol']}" for p in (container.get("Ports") or [])])
            names = ', '.join(container.get("Names", []))

            data.append([container_id, image, command, created, status, ports, names])

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return data

def stop_container(name: str):
    cmd = ['podman', 'stop', name]
    result = run_command(cmd, capture_output=True, text=True)

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return result

def remove_container(name: str):
    stop_container(name)
    cmd = ['podman', 'rm', name]
    result = run_command(cmd, capture_output=True, text=True)

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return result