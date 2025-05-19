import docker
from docker.errors import ImageNotFound, NotFound, APIError
from docker.models.containers import Container

client = docker.from_env()

"""
                                                 ,  ,
                                               / \/ \
                                              (/ //_ \_
     .-._                                      \||  .  \
      \  '-._                            _,:__.-"/---\_ \
 ______/___  '.    .--------------------'~-'--.)__( , )\ \
`'--.___  _\  /    |             Here        ,'    \)|\ `\|
     /_.-' _\ \ _:,_          Be Dragons           " ||   (
   .'__ _.' \'-/,`-~`                                |/
       '. ___.> /=,|  Abandon hope all ye who enter  |
        / .-'/_ )  '---------------------------------'
        )'  ( /(/
             \\ "
              '=='
"""

def show_container(container_name: str) -> dict:
    container: Container
    status = "found"
    try:
        container = client.containers.get(container_name)
        result = {
            "status": status,
            "container_name": container.name,
            "container_id": container.id,
            "container_status": container.status,
            "container_ports": container.ports,
        }
        return result
    except NotFound:
        print(f"{__name__} :: No such container")
        status = "not-found"
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err)
        status = "docker-failed"
    return {"status": status}


def get_container(container_name: str) -> Container | None:
    try:
        return client.containers.get(container_name)
    except NotFound:
        print(f"{__name__} :: No such container")
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err)
    return None


def list_containers() -> list[str] | None:
    running_containers: list
    try:
        running_containers = client.containers.list()
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err)
        return None
    return [container.name for container in running_containers]


def prune() -> int:
    print(f"{__name__} :: Pruning...")
    try:
        client.containers.prune()
        print(f"{__name__} :: Pruned successfully!")
        return 1
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err)
        return 0


def check_server() -> int:
    print(f"{__name__} :: Checking Docker daemon...")
    try:
        client.ping()
        print(f"{__name__} :: Docker daemon is alive!")
        return 1
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err)
        return 0


def restart_container(container_name: str) -> dict | None:
    existing_container = get_container(container_name)
    try:
        existing_container.start()
        return {"container-name": container_name, "container-status": "restarted"}
    except APIError as err:
        if err.is_client_error():
            print(f"{__name__} :: Client-side error - {err.status_code}")
            print(err.explanation)
        else:
            print(f"{__name__} :: Docker-side error - {err.status_code}")
            print(err.explanation)
        return None


def stop_container(container_name: str) -> dict[str, str]:
    status: str
    print(f"{__name__} :: Stopping {container_name}...")
    try:
        client.containers.get(container_name).kill()
        status = "exited"
        print(f"{__name__} :: Stopped {container_name}!")
    except NotFound:
        print(f"{__name__} :: No such container")
        status = "not-found"
    except APIError as err:
        print(f"{__name__} :: Docker-side error - {err.status_code}")
        print(err, err.status_code)
        status = "docker-failed"
    return {"container-name": container_name, "container-status": status}


def start_container(service_type: str, host_port: int, container_port: int, proto: str) -> dict[str, str]:
    container_name = f"blackwall-{service_type}"
    try:
        print(f"{__name__} :: Starting {service_type} at {proto}/{host_port}")
        container: Container = client.containers.run(f"arcadia16/{container_name}:latest",
                                                     name=f"{container_name}",
                                                     ports={f'{container_port}/{proto}': host_port},
                                                     detach=True)
        print(container.name, container.status)
        return {"container-name": container.name, "container-status": container.status}
    except ImageNotFound:
        print(f"{__name__} :: No such image")
        return {"container-name": container_name, "container-status": "not-found"}
    except APIError as err:
        if err.is_client_error():
            print(f"{__name__} :: Client-side error - {err.status_code}")
            if "already in use" in err.explanation:
                print(f"{__name__} :: Container name in use, checking if it is running...")
                if container_name in list_containers():
                    print(f"{__name__} :: Container is alive, no need to restart.")
                    return {"container-name": container_name, "container-status": "already-running"}
                else:
                    result = restart_container(container_name)
                    if result:
                        print(f"{__name__} :: Restart successful!")
                        return result
                    else:
                        print(f"{__name__} :: Failed to restart container!")
            else:
                print(err.explanation)
        else:
            print(f"{__name__} :: Docker-side error - {err.status_code}")
            print(err.explanation)
        return {"container-name": container_name, "container-status": "docker-failed"}
