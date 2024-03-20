from app import app

@app.route("/")
def index_route():
    return "<p>Hello World</p>"
