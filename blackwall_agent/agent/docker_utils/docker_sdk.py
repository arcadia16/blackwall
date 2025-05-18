import docker
from .dockerfile_repo import image_map

client = docker.from_env()
base_image = "ubuntu:latest"


def test_docker():
    print(client.containers.run("ubuntu:latest", "echo Hello World"))