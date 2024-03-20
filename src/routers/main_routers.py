from src.app import app
from flask import render_template

@app.route("/")
def index_route():
    render_template("index.html")
