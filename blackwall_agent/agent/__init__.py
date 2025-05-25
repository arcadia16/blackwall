from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, status
from .routers import agent_api

app = FastAPI()

# Whitelisted IPs
WHITELISTED_IPS = [
    "192.168.1.64"
]


@app.middleware('http')
async def validate_ip(request: Request, call_next):
    # Get client IP
    ip = str(request.client.host)
    print("Validating incoming IP", ip)
    # Check if IP is allowed
    if ip not in WHITELISTED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=data)
    print("Validator: OK")
    # Proceed if IP is allowed
    return await call_next(request)
