# from ..config import <settings>
# save files from server to ..honeypot_docker_repo.<honeypot_type>
# save configuration POST to configuration.json
# make GET function to receive ssh_pubkey by agent_i
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from requests import get as r_get, ConnectionError as RequestConnectionError  # , Response

from ..config import MASTER_SERVER_IP, MASTER_SERVER_PORT

router = APIRouter(
    prefix="/agent"
)


@router.get("/")
async def index():
    return JSONResponse(content={})


@router.get("/check_server")
async def check_server(request: Request):
    print("Incoming connection from", request.client.host)
    try:
        r_get(f"http://{MASTER_SERVER_IP}:{MASTER_SERVER_PORT}", timeout=5, verify=False)
    except RequestConnectionError:
        print("Server unavailable")
        return JSONResponse(content={"server": "down"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return JSONResponse(content={"server": "up"})
