import os
from flask import Flask, render_template, send_from_directory
from flask_wtf.csrf import CSRFProtect
from src.forms import MainForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

csrf = CSRFProtect(app)


@app.route("/")
def index():
    form = MainForm()
    return render_template("index.html", form=form)


@app.route("/images/<filename>")
def image(filename):
    return send_from_directory("images", filename)


@app.route("/modify", methods=["POST"])
def modify():
    pass


if __name__ == "__main__":
    app.run(debug=True)
