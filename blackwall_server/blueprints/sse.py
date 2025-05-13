from flask import Blueprint
from flask import Response, request
import queue
import threading
from uuid import uuid4
import json
from blackwall_server.logs.logger import log_to_file

bp = Blueprint('sse', __name__, url_prefix='/sse')

# TODO: Make WebClient class to track remote_ip and lessen amount of requests
# CHANGE MODULE NAMING

# Track active clients: {client_id: queue}
clients = {}
lock = threading.Lock()


def event_stream(client_id):
    while True:
        try:
            # Get message from THIS client's queue (non-blocking)
            message = clients[client_id].get(timeout=10)
            yield f"data: {message}\n\n"
        except queue.Empty:
            # Send keep-alive to prevent connection timeout
            yield ":keepalive\n\n"
        except KeyError:
            # Client disconnected
            break


@bp.route("/stream")
def sse_stream():
    fn = f"sse:{sse_stream.__name__}"
    client_id = str(uuid4())  # Unique ID for this client
    # Create a dedicated queue for this client
    # TODO: Pre WebClient class - check for doubled sessions from same IP and close the oldest
    print(f"{fn} Registered new client {client_id} from {request.remote_addr}")
    with lock:
        clients[client_id] = queue.Queue()
    print(f"{fn} Total clients: {len(clients)}")
    log_to_file('sse.log', __name__, f"Registered new client {client_id} from {request.remote_addr}")

    # Stream messages to client
    def generate():
        try:
            for message in event_stream(client_id):
                yield message
        finally:
            # Cleanup on disconnect
            with lock:
                del clients[client_id]

    return Response(generate(), mimetype="text/event-stream")


@bp.route("/send", methods=["POST"])
def send_message():
    fn = f"sse:{send_message.__name__}"
    print(f"{fn} Incoming request from {request.remote_addr}")
    data: dict = request.json
    # Here will come messages from agents
    # TODO: Separate classes for states DEAD, BRCH, WARN, GOOD, make switch function
    #  Need to make a parser for requests, decide on fields and probably write a module for it
    #  Add faculty \ severity to messages?
    data["from"] = request.remote_addr
    message = json.dumps(data)
    print(f"{fn} Content - {message}")
    log_to_file('sse.log', __name__, message)
    # Broadcast to ALL clients
    with lock:
        for client_id in list(clients.keys()):  # Avoid RuntimeError
            try:
                print(f"{fn} Putting message to {client_id}")
                clients[client_id].put(message)
            except:
                del clients[client_id]

    return {"status": "Broadcasted"}, 200
