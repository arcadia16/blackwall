from random import choice
from time import sleep

from flask_restful import Resource
from blackwall_server.logs import logger


class AgentAPI(Resource):
    def get(self, agent_id: int):
        logger.request_log(__name__)
        sleep(3)
        return {"AGENT_ID": agent_id, "STATE": choice([200, 300, 400])}, 200
