from flask import render_template, request
from flask_sse import sse
from blackwall_server import app

app.register_blueprint(sse, url_prefix='/stream')

@app.route('/')
def index():
    return render_template('index.html', agents=[1, 2, 3, 4])

@app.route('/health')
def health_monitoring():
    # TODO: Write Redis server connectivity check
    return "OK"


@app.route('/hello')
def publish_hello():
    sse.publish({"status": "ready"}, type="publish")
    return "Message sent!"


@app.route('/send', methods=['POST'])
def send_data():
    sse.publish(request.json)
    return "Sent"
