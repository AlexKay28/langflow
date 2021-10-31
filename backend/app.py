import json

from flask import Flask
from flask_cors import CORS

from api import api


app = Flask(__name__)
app.register_blueprint(api)
CORS(app)


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
