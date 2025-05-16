from random import choice
from time import sleep

from flask import request
from flask_restful import Resource
# from .AgentInterface import AgentInterface
# from ..logger import api_log, log_to_file

registered_agents = {}


class AgentAPI(Resource):
    def get(self, agent_id: str = None):
        if agent_id is None:
            return 200
        # api_log(__name__, self.get, agent_id)
        # log_to_file('request.log', __name__)
        sleep(3)
        # TODO: Agent connection + Agent class
        return {"AGENT_ID": agent_id, "STATE": choice([200, 300, 400])}

    def post(self, agent_id: str):
        # api_log(__name__, self.post, agent_id)
        # log_to_file('request.log', __name__)
        if registered_agents.get(agent_id) is None:
            registered_agents[agent_id] = request.remote_addr
        print(request.remote_addr, request.json)
        return {}, 201
