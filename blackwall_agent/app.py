from uuid import uuid4
from json import loads as j_loads
import uvicorn
from requests import post as r_post, ConnectionError as RequestConnectionError

from agent import app
from agent.routers import agent_api, docker_api
from agent.config import MASTER_SERVER_IP

app.include_router(agent_api.router)
app.include_router(docker_api.router)

AGENT_ID = str(uuid4())
REGISTRATION_STATE: bool = False


if __name__ == '__main__':
    try:
        response = r_post(MASTER_SERVER_IP + f"/agent/{AGENT_ID}",
                          json={"agent_status": "launched"},
                          timeout=5)
        if response.status_code == 201:
            print("Registered on server!")
            REGISTRATION_STATE = True
        else:
            if response.status_code == 200:
                print("Already registered", response.text)
                AGENT_ID = j_loads(response.text).get("agent_id")
                REGISTRATION_STATE = True
    except RequestConnectionError:
        print("Server unavailable!")
    uvicorn.run("app:app", host="0.0.0.0", port=8091,
                log_level="info", ssl_certfile="agent/certs/public_certificate.pem", ssl_keyfile="agent/certs/private_key.pem")
