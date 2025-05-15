import json
from typing import List

from Managers.log_manager import LogManager
from Managers.system_manager import run_command


def list_networks() -> List[List[str]]:
    """
    List all podman networks.
    :return: A list of networks with their details.
    """
    # The command to list all images in the system in JSON format
    cmd = ["podman", "network", "ls", "--format", "json"]

    # The headers for the table
    headers = ["Network ID", "Name", "Driver", "Subnet(s)"]
    data = [headers]

    # Run the command and capture the output
    result = run_command(cmd, capture_output=True, text=True)
    # If the command was successful, parse the JSON output
    if result.returncode == 0:
        # The JSON output is stored in result.stdout
        content = json.loads(result.stdout)
        # Iterate through the images and extract the relevant information
        for image in content:
            # Extract the repository, tag, and ID
            network_id = image.get("id")[:12]
            name = image.get("name")
            driver = image.get("driver")
            subnets = [x["subnet"] for x in image.get("subnets")]
            data.append([network_id, name, driver, ", ".join(subnets)])

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the data
    return data

def create_network(name: str, subnet: str):
    # Create a new podman network with the given name and subnet
    cmd = ['podman', 'network', 'create', '--subnet', subnet, name]
    result = run_command(cmd, capture_output=True, text=True)

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result of the command
    return result

def remove_network(name: str):
    # Remove a podman network with the given name
    cmd = ['podman', 'network', 'rm', name]
    result = run_command(cmd, capture_output=True, text=True)

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result of the command
    return result
