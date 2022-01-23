import json

from flask import Flask
from flasgger import Swagger

from api import api

app = Flask(__name__)
app.register_blueprint(api)
Swagger(app)

if __name__ == "__main__":
    app.run(host="localhost", port=6769, debug=True)
