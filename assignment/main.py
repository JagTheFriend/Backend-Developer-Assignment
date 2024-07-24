from flask import Flask
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
