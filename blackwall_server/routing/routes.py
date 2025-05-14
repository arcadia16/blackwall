from flask import render_template, request, jsonify
from flask_sse import sse
from blackwall_server import app
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/')
def index():
    return render_template('index.html', agents=[1, 2, 3, 4])

@app.route('/health')
def health_monitoring():
    # TODO: Write Redis server connectivity check
    return "OK", 200


@app.route('/hello')
def publish_hello():
    sse.publish({"status": "ready"}, type="publish", retry=15)
    return "Hello"


@app.route('/send', methods=['POST'])
def send_data():
    try:
        data = request.json
        sse.publish(data, type="publish")

        return jsonify(status="success", message="published", data=data)
    except:
        return jsonify(status="fail", message="not published")

@app.route('/receive', methods=['POST'])
def receive_data():
    print(request.json)
    return "Got"