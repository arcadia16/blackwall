from flask_restful import Resource


class ConfiguratorAPI(Resource):
    def get(self):
        return 'Hello Configurator!'
