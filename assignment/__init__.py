from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"

@app.route("/retreats", methods= ["GET"])
def get_retreats():
    return {
        "data": []
    }

@app.route("/retreats/book", methods= ["POST"])
def create_retreat():
    return {
        "data": []
    }

if __name__ == "__main__":
    app.run(debug=True)
