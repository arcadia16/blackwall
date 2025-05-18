#from random import choice
#from time import sleep

from flask import request #jsonify
from flask_restful import Resource
from requests import get as r_get, Response, ConnectionError as RequestConnectionError

# from .AgentInterface import AgentInterface
# from ..logger import api_log, log_to_file

registered_agents = {}
known_clients = {}  # For every agent request an id should be provided, maybe JWT?


def search_by_value(dict_object: dict, dict_value):
    for key in dict_object.keys():
        if dict_object[key] == dict_value:
            return key
    return None

def try_request(request_url: str, timeout: float) -> Response:
    try:
        response = r_get(request_url, timeout=timeout)
    except RequestConnectionError:
        dummy = Response()
        dummy.status_code = 500
        return dummy
    return response

class AgentAPI(Resource):
    def get(self, agent_id: str = None):
        print("Looking for", agent_id)
        if agent_id is None:
            return 400
        target_ip = search_by_value(registered_agents, agent_id)
        print("Target:", target_ip)
        # TODO: Agent connection + Agent class
        response = try_request(f"http://{target_ip}:8091/agent", 15)
        print(response)
        return {"AGENT_ID": agent_id, "STATE": response.status_code}

    def post(self, agent_id: str):
        # TODO: move registration func into separate GET, agent should get UUID from server
        src_ip = request.remote_addr
        print("Agent connecting from", src_ip)
        if registered_agents.get(src_ip) is None:
            registered_agents[src_ip] = agent_id
            print("Registered new agent:", agent_id, "from", src_ip)
            print("Total agents:", registered_agents)
            return {}, 201
        print("Hey, old agent from", src_ip, request.json)
        old_id = registered_agents.get(src_ip)
        return {"agent_id": old_id}
