import json
# from uuid import uuid4
# from time import sleep
from flask import Response, jsonify, request, Blueprint
import redis

from ..config import REDIS_URL, REDIS_CHANNEL
from .data_validator import fix_json

sse_bp = Blueprint("sse_blueprint", __name__)
SSE_FORMAT = "data: {}\n\n"

redis_connector = redis.from_url(REDIS_URL)


@sse_bp.route('/stream')
def sse_stream():
    print(f"{__name__} Subscribing client from {request.remote_addr}")

    def sse_events():
        pubsub = redis_connector.pubsub()
        pubsub.subscribe(REDIS_CHANNEL)
        for message in pubsub.listen():
            try:
                print("Stream ::", message, type(message))
                print("Trying to serialize message")
                print("Fixing channel")
                message = fix_json(message)
                print("Fixed message", message)
                message = str(message).replace("'", '"')
                json.dumps(message)
                if isinstance(message, dict):
                    print("Got JSON")
                yield f"data: {message}\n\n"
            except json.decoder.JSONDecodeError as err:
                print(__name__, err)

    return Response(sse_events(), mimetype="text/event-stream")


@sse_bp.route('/healthmon')
def check_health():
    return {"from": "sse", "status": "good"}, 200


@sse_bp.route('/publish', methods=["POST"])
def publish():
    print(f"{__name__} Receiving message from {request.remote_addr}")
    try:
        data = request.json
        print(fix_json(data))
        print("Publish ::", data, type(data))
        redis_connector.publish(str(REDIS_CHANNEL), json.dumps(data))
        return jsonify(status="success", message="published", channel=REDIS_CHANNEL, data=data)
    except json.JSONDecodeError as err:
        print(__name__, err)
        return jsonify(status="failure", message="not published", channel=REDIS_CHANNEL)
