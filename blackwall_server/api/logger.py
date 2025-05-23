import os
from datetime import datetime
from flask import request
from .config import LOGGING_TIMEFORM, LOGGING_FILEPATH


REQ_LOG_FORM = "{}:{} Incoming {} request from {} for agent {}"


def get_time_now():
    timestamp: datetime = datetime.now()
    return timestamp.strftime(LOGGING_TIMEFORM)


def log(function_name, message: str) -> None:
    print(f"{function_name} :: {message}")


# BREAKS IN DOCKER
def log_to_file(filename: str, function_name: str, message: str = None):
    if filename == "request.log":
        if message is None:
            message = f"{request.method} {request.remote_addr} {request.url}"
        else:
            message = f"{request.method} {request.remote_addr} {request.url} " + message
    with open(LOGGING_FILEPATH + filename, 'a', encoding="utf-8") as logfile:
        logfile.write(
            f"{get_time_now()} {os.getlogin()} {function_name}[{os.getpid()}]: {message}\n")


def api_log(api_name: str, func, agent_id: str) -> None:
    print(REQ_LOG_FORM.format(api_name, func.__name__, request.method, request.remote_addr, agent_id))
