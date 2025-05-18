import docker
from docker import errors

client = docker.from_env()
base_image = "ubuntu:latest"

def build_image(dockerfile_path: str):
    try:
        result = client.images.build(path=dockerfile_path)
        return result
    except errors.BuildError:
        print(f"{__name__} :: Build error for {dockerfile_path}")
        return None
    except errors.APIError:
        print(f"{__name__} :: Unknown Docker error")
        return None
    except TypeError:
        print(f"{__name__} :: Neither path nor fileobj is specified")
        return None

def test_docker():
    print(client.containers.run("ubuntu:latest", "echo Hello World"))

test_docker()