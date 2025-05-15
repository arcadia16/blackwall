from flask import Flask
from flask_restful import Api

# from .resources import <apis>

app = Flask(__name__)
api = Api(app)
# app.config["KEY"] = "VALUE"
# api.add_resource("api_class", "endpoints")
