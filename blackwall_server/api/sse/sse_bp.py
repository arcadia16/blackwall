from flask import Response, jsonify, json, request, Blueprint
import redis
from ..config import REDIS_URL, REDIS_CHANNEL
# from uuid import uuid4
# from time import sleep
from .data_validator import fix_json

sse_bp = Blueprint("sse_blueprint", __name__)
sse_format = "data: {}\n\n"

redis_connector = redis.from_url(REDIS_URL)
redis_channel = REDIS_CHANNEL


@sse_bp.route('/stream')
def sse_stream():
    print(f"{__name__} Subscribing client from {request.remote_addr}")

    def sse_events():
        pubsub = redis_connector.pubsub()
        pubsub.subscribe(redis_channel)
        for message in pubsub.listen():
            try:
                print("Stream ::", message, type(message))
                print("Trying to serialize message")
                print("Fixing channel")
                message = fix_json(message)
                print("Fixed message", message)
                message = str(message).replace("'", '"')
                json.dumps(message)
                if type(message) == dict:
                    print("Got JSON")
                yield f"data: {message}\n\n"
            except Exception as err:
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
        print("Publish ::", data, type(data))
        redis_connector.publish(str(redis_channel), json.dumps(data))
        return jsonify(status="success", message="published", channel=redis_channel, data=data)
    except Exception as err:
        print(__name__, err)
        return jsonify(status="failure", message="not published", channel=redis_channel)
