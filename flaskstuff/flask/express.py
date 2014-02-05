from blueprints import Blueprint
from app import Flask

class FlaskExpress(Flask):

    def register_route(self, route):
        self.register_blueprint(route)

class Route(Blueprint):

    def get(self, url, function):
        Blueprint.add_url_rule(self, url, function.__name__, function, methods=['GET'])

    def post(self, url, function):
        Blueprint.add_url_rule(self, url, function.__name__, function, methods=['POST'])

    def put(self, url, function):
        Blueprint.add_url_rule(self, url, function.__name__, function, methods=['PUT'])

    def delete(self, url, function):
        Blueprint.add_url_rule(self, url, function.__name__, function, methods=['DELETE'])