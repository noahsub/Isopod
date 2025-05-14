########################################################################################################################
# image_manager.py
# This module provides functionality for management of Podman images.
#
# Copyright (c) 2025 noahsub
########################################################################################################################


########################################################################################################################
# IMPORTS
########################################################################################################################
import json
import pprint
from datetime import datetime, timezone
from pathlib import Path
from subprocess import CompletedProcess
from typing import List
import requests
from Managers.log_manager import LogManager
from Managers.system_manager import run_command


########################################################################################################################
# LOCAL IMAGE FUNCTIONS
########################################################################################################################
def list_images() -> List[List[str]]:
    """
    List all images stored on the system.
    :return: A list of images with their details.
    """
    # The command to list all images in the system in JSON format
    cmd = ["podman", "images", "--format", "json"]

    # The headers for the table
    headers = ["Repository", "Tag", "Image ID", "Created", "Size"]
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
            if len(image.get("Names", [])) > 0:
                repository, tag = image["Names"][0].split(":")
            else:
                repository, tag = "Unknown", "Unknown"
            img_id = image["Id"][:12]
            # Parse the creation date
            created = datetime.fromtimestamp(
                image["Created"], tz=timezone.utc
            ).strftime("%Y-%m-%d")
            # Convert the size from bytes to MB
            size = f"{round(image['Size'] / (1024 ** 2), 2)} MB"
            # Append the image details to the data list
            data.append([repository, tag, img_id, created, size])

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the data
    return data


def remove_image(img_id: str):
    """
    Remove an image from the system if it is not in use.
    :param img_id: The ID of the image to remove.
    :return: A CompletedProcess object containing the result of the command.
    """
    # The command to remove the image
    result = run_command(
        ["podman", "image", "rm", img_id], capture_output=True, text=True
    )

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result
    return result


########################################################################################################################
# REGISTRY FUNCTIONS
########################################################################################################################
def fetch_top_docker_hub_images(n: int = 25) -> List[List[str]]:
    """
    Fetch the top N Docker Hub images from the library repository.
    :param n: The number of images to fetch.
    :return: A list of images with their details.
    """
    # The URL for the Docker Hub API
    url = "https://hub.docker.com/v2/repositories/library/"

    # Request the top N images
    response = requests.get(url, params={"page": 1, "page_size": n})
    response.raise_for_status()

    # Parse the response
    data = [["Repository", "Official", "Pull Count", "Star Count", "Description"]]
    # Iterate through the results and extract the relevant information
    for result in response.json().get("results", []):
        data.append(
            [
                # Extract the repository name
                result.get("name", "Unknown"),
                # Official since it's in 'library'
                "Yes",
                # Extract the pull count and star count
                result.get("pull_count", 0),
                result.get("star_count", 0),
                # Extract the description
                result.get("description", "No description available"),
            ]
        )

    # Return the data
    return data


def search_docker_hub_images(query: str) -> List[List[str]]:
    """
    Search for Docker Hub images based on a query.
    :param query: The name or keyword to search for.
    :return: A list of images with their details.
    """
    # The URL for the Docker Hub API
    url = "https://hub.docker.com/v2/search/repositories/"

    # Request the images based on the query
    response = requests.get(url, params={"query": query})
    response.raise_for_status()

    # Parse the response
    data = [["Repository", "Official", "Pull Count", "Star Count", "Description"]]
    # Iterate through the results and extract the relevant information
    for result in response.json().get("results", []):
        data.append(
            [
                # Extract the repository name
                result.get("repo_name", "Unknown"),
                # Check if the image is official
                "Yes" if result.get("is_official", False) else "No",
                # Extract the pull count and star count
                result.get("pull_count", 0),
                result.get("star_count", 0),
                # Extract the description
                result.get("short_description", "No description available"),
            ]
        )

    return data


def get_docker_hub_tags(repository: str, max_tags: int = 10) -> List[List[str]]:
    """
    Fetch the tags for a given Docker Hub repository.
    :param repository: The name of the repository (e.g., 'library/alpine').
    :param max_tags: The maximum number of tags to fetch.
    :return: A list of tags with their details.
    """
    # Determine the url for the specified image
    namespace, repo_name = (
        repository.split("/") if "/" in repository else ("library", repository)
    )
    tags_url = f"https://hub.docker.com/v2/repositories/{namespace}/{repo_name}/tags/"

    # Request the tags for the repository
    response = requests.get(tags_url, params={"page_size": max_tags})
    response.raise_for_status()

    # Parse the response
    data = [["Repository", "Tag", "Date Created"]]
    # Iterate through the results and extract the relevant information
    for tag in response.json().get("results", []):
        data.append(
            [
                # Extract the repository name
                repository,
                # Extract the tag name
                tag.get("name", "Unknown"),
                # Extract the date created and format it to a readable format
                datetime.fromisoformat(
                    tag.get("last_updated", "1970-01-01T00:00:00Z").replace(
                        "Z", "+00:00"
                    )
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
            ]
        )

    # Return the data
    return data


def get_image_url(source: str, repository: str, tag: str = "latest") -> str:
    """
    Generate the image URL based on the source, repository, and tag.
    :param source: The source of the image (e.g., 'docker.io').
    :param repository: The name of the repository (e.g., 'library/alpine').
    :param tag: The tag of the image (default is 'latest').
    :return: The formatted image URL.
    """
    # Determine the namespace and repository name
    namespace, repo_name = (
        repository.split("/") if "/" in repository else ("library", repository)
    )

    # Generate the image URL based on the source
    match source:
        case "docker.io":
            return f"{source}/{namespace}/{repo_name}:{tag}"

    # If the source is not recognized, return an empty string
    return ""


def pull_image(source: str, repository: str, tag: str = "latest") -> CompletedProcess:
    """
    Pull an image from a specified source and repository.
    :param source: The source of the image (e.g., 'docker.io').
    :param repository: The name of the repository (e.g., 'library/alpine').
    :param tag: The tag of the image (default is 'latest').
    :return: A CompletedProcess object containing the result of the command.
    """
    # Generate the image URL
    url = get_image_url(source, repository, tag)

    # Attempt to pull the image
    result = run_command(
        ["podman", "pull", "--quiet", url], capture_output=True, text=True
    )

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result
    return result


########################################################################################################################
# BUILDING FUNCTIONS
########################################################################################################################

def build_image(path: Path, name: str, tag: str = "latest") -> CompletedProcess:
    """
    Build a Docker image from a specified directory.
    :param path: The path to the directory containing the Dockerfile and resources.
    :param name: The name of the image to build.
    :param tag: The tag of the image (default is 'latest').
    :return: A CompletedProcess object containing the result of the command.
    """
    # Attempt to build the image
    result = run_command(["podman", "build", "--rm", "--no-cache", "-t", f"{name}:{tag}", str(path)], capture_output=True, text=True)

    # Log the operation
    log_manager = LogManager()
    log_manager.write_system_log(result)

    # Return the result
    return result