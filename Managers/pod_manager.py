import json
from datetime import datetime, timezone
from typing import List

from Managers.log_manager import LogManager
from Managers.system_manager import run_command


def list_pods() -> List[List[str]]:
    """
    List all podman pods.
    :return: A list of pods with their details.
    """
    # The command to list all images in the system in JSON format
    cmd = ["podman", "pod", "ps", "--format", "json"]

    # The headers for the table
    headers = ["Pod ID", "Name", "Status", "Created", "Infra ID", "# of Containers", "Network(s)"]
    data = [headers]

    # Run the command and capture the output
    result = run_command(cmd, capture_output=True, text=True)
    # If the command was successful, parse the JSON output
    if result.returncode == 0:
        # The JSON output is stored in result.stdout
        content = json.loads(result.stdout)
        # Iterate through the images and extract the relevant information
        for pod in content:
            pod_id = pod.get("Id")[:12]
            pod_name = pod.get("Name")
            pod_status = pod.get("Status")
            pod_created = datetime.fromisoformat(pod.get("Created")).astimezone(timezone.utc).strftime("%Y-%m-%d")
            pod_infra_id = pod.get("InfraId")[:12]
            pod_containers = str(len(pod.get("Containers")))
            pod_networks = ','.join(pod.get("Networks"))
            data.append([pod_id, pod_name, pod_status, pod_created, pod_infra_id, pod_containers, pod_networks])

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the data
    return data

def create_pod(name: str, network: str =''):
    # Create a new podman pod with the given name and network
    cmd = ['podman', 'pod', 'create', '--network', network, name]
    result = run_command(cmd, capture_output=True, text=True)

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result of the command
    return result

def remove_pod(name: str):
    # Remove a podman pod with the given name
    cmd = ['podman', 'pod', 'rm', name]
    result = run_command(cmd, capture_output=True, text=True)

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result of the command
    return result
