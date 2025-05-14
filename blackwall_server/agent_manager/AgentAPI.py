from random import choice
from time import sleep

from flask import request
from flask_restful import Resource

from blackwall_server.logs import logger
from blackwall_server.agent_manager.AgentInterface import AgentInterface

registered_agents = {}
api_fullname = "agent_manager.AgentAPI.AgentAPI"

class AgentAPI(Resource):
    def get(self, agent_id: str = None):
        if agent_id is None:
            return 200
        logger.api_log(api_fullname, self.get, agent_id)
        logger.log_to_file('request.log', __name__)
        sleep(3)
        # TODO: Agent connection + Agent class
        return {"AGENT_ID": agent_id, "STATE": choice([200, 300, 400])}

    def post(self, agent_id: str):
        logger.api_log(api_fullname, self.post, agent_id)
        logger.log_to_file('request.log', __name__)
        if registered_agents.get(agent_id) is None:
            registered_agents[agent_id] = request.remote_addr
        print(request.remote_addr, request.json)
        return {}, 201
