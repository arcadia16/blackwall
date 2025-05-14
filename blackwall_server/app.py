from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from flask_sse import sse
from config import REDIS_URL
from agent_manager.AgentAPI import AgentAPI
from configuration_manager.ConfiguratorAPI import ConfiguratorAPI

app = Flask(__name__)
api = Api(app)
app.config["REDIS_URL"] = REDIS_URL

api.add_resource(AgentAPI, '/agent', '/agent/<string:agent_id>')
api.add_resource(ConfiguratorAPI, '/cfg')

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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
