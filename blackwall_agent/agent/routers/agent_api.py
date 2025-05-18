# from ..config import <settings>
# save files from server to ..honeypot_docker_repo.<honeypot_type>
# save configuration POST to configuration.json
# make GET function to receive ssh_pubkey by agent_i
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from requests import get as r_get, ConnectionError as RequestConnectionError#, Response

from ..config import MASTER_SERVER_IP

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
        r_get(MASTER_SERVER_IP, timeout=5)
    except RequestConnectionError:
        print("Server unavailable")
        return JSONResponse(content={"server": "down"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return JSONResponse(content={"server": "up"})
