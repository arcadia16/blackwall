from flask import Flask
from flask_restful import Api
from blackwall_server.agent_manager.AgentAPI import AgentAPI
from blackwall_server.configuration_manager.ConfiguratorAPI import ConfiguratorAPI

app = Flask(__name__)
api = Api(app)

from blackwall_server.routing import routes
from blackwall_server.blueprints.sse import bp as sse_bp

api.add_resource(AgentAPI, '/agent/<string:agent_id>')
api.add_resource(ConfiguratorAPI, '/cfg')

app.register_blueprint(sse_bp)
