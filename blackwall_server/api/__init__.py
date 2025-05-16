from flask import Flask
from flask_restful import Api
from .routes import api_bp
from .sse.sse_bp import sse_bp
from .config import REDIS_URL, REDIS_CHANNEL
from .agent_manager.agent_api import AgentAPI
from .configuration_manager.configurator_api import ConfiguratorAPI


def create_flask_app():
    app = Flask(__name__)
    api = Api(app)

    # CORS??
    app.config["REDIS_URL"] = REDIS_URL
    app.config["REDIS_CHANNEL"] = REDIS_CHANNEL

    api.add_resource(AgentAPI, '/agent', '/agent/<string:agent_id>')
    api.add_resource(ConfiguratorAPI, '/cfg')

    app.register_blueprint(api_bp, url_prefix='/')
    app.register_blueprint(sse_bp, url_prefix='/sse')
    return app
