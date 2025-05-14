from queue import Queue
from flask import Blueprint
from flask import Response, request
import queue
import threading
from uuid import uuid4
import json
from blackwall_server.logs.logger import log_to_file, log

bp = Blueprint('sse', __name__, url_prefix='/sse')

# TODO: Make WebClient class to track remote_ip and lessen amount of requests
# CHANGE MODULE NAMING
# Buggy af, need to write simpler

# Track active clients: {client_id: queue}
clients = {}
lock = threading.Lock()
id_cookie_field = "blackwall_client-id"
cookie_max_age = 60 * 60 * 24 * 7  # 7 days

def event_stream(client_id):
    while True:
        try:
            # Get message from THIS client's queue (non-blocking)
            message = clients[client_id].get(timeout=5)
            print("Processing message for", client_id)
            yield f"data: {message}\n\n"
        except queue.Empty:
            # Send keep-alive to prevent connection timeout
            # yield ":keepalive\n\n"
            yield ":\n\n"
        except KeyError:
            print("EEREHR")
            # Client disconnected
            break


# Stream messages to client
def generate(client_id: str):
    try:
        for message in event_stream(client_id):
            print(f"Generate :: process message {message} for {client_id}")
            yield message
    finally:
        # Cleanup on disconnect
        with lock:
            print(f"Generate :: Trying to delete {client_id} from {clients}")
            del clients[client_id]


def get_client_id_from_cookie():
    return request.cookies.get(id_cookie_field)


def check_queue(client_id: str, is_new: bool = False) -> None:
    with lock:
        if is_new:
            log(__name__, f"New queue for {client_id}")
            clients[client_id] = Queue()
        else:
            if not clients.get(client_id):
                log(__name__, f"Warning: no message queue found for {client_id}, making new one.")
                clients[client_id] = Queue()


def generate_response(client_id: str, set_cookie: bool = False) -> Response:
    print(f"Set cookie {__name__} {clients}")
    response_object = Response(generate(client_id), mimetype="text/event-stream")
    if set_cookie:
        response_object.set_cookie(key=id_cookie_field, value=client_id, max_age=cookie_max_age)
    return response_object


@bp.route("/")
def index(): return {}, 200

@bp.route("/stream")
def sse_stream():
    client_id = get_client_id_from_cookie()
    # TODO: Pre WebClient class - check for doubled sessions from same IP and close the oldest
    if client_id:
        log(__name__, f"Known client {client_id} from {request.remote_addr}")
        check_queue(client_id)
        log(__name__, f"Total clients: {len(clients)}")
        return generate_response(client_id)
    else:
        client_id = str(uuid4())  # Unique ID for new client
        log(__name__, f"New client {client_id} from {request.remote_addr}")
        check_queue(client_id, True)
        log_to_file('sse.log', __name__, f"Registered new client {client_id} from {request.remote_addr}")
        return generate_response(client_id, True)


@bp.route("/receive", methods=["POST"])
def receive_message():
    print(f"Received: {request.json}")
    return "Accepted", 200

@bp.route("/send", methods=["POST"])
def send_message():
    print(f"Sent {__name__} {clients}")
    data: dict = request.json
    # Here will come messages from agents
    # TODO: Separate classes for states DEAD, BRCH, WARN, GOOD, make switch function
    #  Need to make a parser for requests, decide on fields and probably write a module for it
    #  Add faculty \ severity to messages?
    data["from"] = request.remote_addr
    message = json.dumps(data)
    log(__name__, f"Incoming request from {request.remote_addr} with {message}")
    log_to_file('sse.log', __name__, message)
    # Broadcast to ALL clients
    with lock:
        if len(clients) > 0:
            for client_id in list(clients.keys()):  # Avoid RuntimeError
                try:
                    log(__name__, f"Putting message in {client_id} queue")
                    clients[client_id].put_nowait(message)
                except Exception as error:
                    print(f"Send Trying to delete {client_id} from {clients} because {error}")
                    del clients[client_id]
            return {"status": "Broadcasted"}, 200
        return {"status": "No clients present"}, 202
