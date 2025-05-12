from flask import Flask
from flask_restful import Api
from blackwall_server.resources.AgentAPI import AgentAPI

app = Flask(__name__)
api = Api(app)

from blackwall_server.routing import routes

api.add_resource(AgentAPI, '/ag/<int:agent_id>')
