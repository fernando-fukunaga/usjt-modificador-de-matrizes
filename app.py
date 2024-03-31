from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/images/<filename>")
def image(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run(debug=True)
