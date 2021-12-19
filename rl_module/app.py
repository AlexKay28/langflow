import json

from flask import Flask
from flasgger import Swagger

from api import api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.register_blueprint(api)
Swagger(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:123456@localhost:5432/langflow"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="localhost", port=6768, debug=True)
