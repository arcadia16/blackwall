from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..docker_utils.docker_sdk import start_container, stop_container, prune, check_server, list_containers, \
    show_container
from ..docker_utils.service_mapping import ports

router = APIRouter(
    prefix="/docker"
)


@router.get("/")
async def server():
    server_status = "ok"
    if not check_server():
        server_status = "down"
    return JSONResponse({"server-health": server_status})


@router.get("/container/{container_name}")
async def container_info(container_name: str):
    container_information = show_container(container_name)
    search_status = container_information.get("status")
    status_code: int = 200
    if search_status == "not-found":
        status_code = 404
    if search_status == "docker-failed":
        status_code = 500
    return JSONResponse(container_information, status_code)


@router.get("/start/{service_name}")
async def start_service(service_name: str):
    # TODO: Probably should rewrite as POST and pass ports in form
    if ports.get(service_name) is None:
        return JSONResponse({"status": "no-such-service"}, 404)
    result = start_container(service_name, *ports[service_name].values())
    # Stream logs to REDIS?
    return JSONResponse(result, 200)


@router.get("/stop/{container_name}")
async def stop_service(container_name: str):
    status = 200
    result = stop_container(container_name)
    if result.get("container-status") == "not-found":
        status = 404
    if result.get("container-status") == "docker-failed":
        status = 500
    return JSONResponse(content=result, status_code=status)


@router.get("/prune")
async def clear_containers():
    if prune():
        return JSONResponse({"status": "cleared"}, 200)
    else:
        return JSONResponse({"status": "docker-failed"}, 500)


@router.get("/list-all")
async def list_running():
    return JSONResponse({"running": list_containers()})

# @router.get("/container/{container_name}/logs") # Probably works
# async def show_container_logs(container_name: str):
#     return StreamingResponse(content=container_logs_stream(container_name),
#                              media_type="text/event-stream")