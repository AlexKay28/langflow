import os
import json

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from dotenv import load_dotenv

load_dotenv(".env")

from api import api
from dbase import db

app = Flask(__name__)
app.register_blueprint(api)
Swagger(app)
CORS(app)

POSTGRES_HOST = os.getenv('POSTGRES_HOST', "localhost")
POSTGRES_PORT = os.getenv('POSTGRES_PORT', "5432")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:123456@{POSTGRES_HOST}:{POSTGRES_PORT}/langflow"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6767, debug=True)
