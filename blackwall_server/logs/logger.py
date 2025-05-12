import os

from blackwall_server import config
from datetime import datetime, date
from flask import request


def request_log(function_name):
    with open(config.LOGGING_FILEPATH, 'a') as logfile:
        req_str = f"{request.method} {request.remote_addr} {request.url}\n"
        logfile.write(
            f"{datetime.now().strftime(config.LOGGING_TIMEFORM)} {os.getlogin()} {function_name}[{os.getpid()}]: {req_str}")
