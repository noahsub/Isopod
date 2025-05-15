import json
from datetime import datetime, timezone
from typing import List
from Managers.log_manager import LogManager
from Managers.system_manager import run_command


def list_volumes() -> List[List[str]]:
    """
    List all podman volumes with their details.
    :return: A list of volumes with their details.
    """
    cmd = ["podman", "volume", "ls", "--format", "json"]

    headers = ["Volume Name", "Driver", "Mountpoint", "Created", "Labels"]
    data = [headers]

    result = run_command(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        content = json.loads(result.stdout)
        for volume in content:
            volume_name = volume.get("Name")
            driver = volume.get("Driver")
            mountpoint = volume.get("Mountpoint")
            created = datetime.fromisoformat(volume.get("CreatedAt")).astimezone(timezone.utc).strftime("%Y-%m-%d")
            labels = ', '.join(volume.get("Labels", {}).keys())

            data.append([volume_name, driver, mountpoint, created, labels])

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return data

def create_volume(name: str):
    cmd = ['podman', 'volume', 'create', name]
    result = run_command(cmd, capture_output=True, text=True)

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return result

def remove_volume(name: str):
    cmd = ['podman', 'volume', 'rm', name]
    result = run_command(cmd, capture_output=True, text=True)

    log_manager = LogManager()
    log_manager.write_system_log(result)

    return result
