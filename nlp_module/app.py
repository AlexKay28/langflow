import json

from flask import Flask
from flasgger import Swagger

from dotenv import load_dotenv

load_dotenv(".env")

from api import api

app = Flask(__name__)
app.register_blueprint(api)
Swagger(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6769, debug=True)
