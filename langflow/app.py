import json

from flask import Flask, render_template, url_for, request, redirect

from utils.session import SessionController

from api import api

app = Flask(__name__)
app.register_blueprint(api)

session = SessionController()


@app.route("/", methods=["POST", "GET"])
def home_page():
    """
    Main page of LangFlow
    """
    if request.method == "POST":  # make GET
        return redirect("/practice")
    return render_template("index.html")


@app.route("/practice", methods=["GET"])  # it will be removed soon
def practice_page():
    """
    Practicing page # make GET
    """
    return render_template("practice.html")


if __name__ == "__main__":
    app.run(host="localhost", port=6767, debug=True)
