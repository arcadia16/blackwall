from flask import render_template, request, Blueprint
from .agent_manager.agent_api import registered_agents

api_bp = Blueprint('api_blueprint', __name__)


@api_bp.route('/')
def index():
    print(registered_agents)
    return render_template('index.html', agents=registered_agents)


@api_bp.route('/health')
def health_monitoring():
    # TODO: Write Redis server connectivity check
    return {"from": "api", "status": "good"}, 200


@api_bp.route('/receive', methods=['POST'])
def receive_data():
    print(request.json)
    return "Got"
