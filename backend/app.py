import json

from flask import Flask, render_template, url_for, request, redirect

from api import api

from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api)
CORS(app)


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
