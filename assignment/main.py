from flask import Flask, request, Response, jsonify
from database import db, BookingsTable
from sqlalchemy import exc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/retreats", methods=["GET"])
def get_retreats():
    return {"data": []}


@app.route("/retreats/book", methods=["POST"])
def book_retreat():
    request_data = request.get_json()

    user_id = request_data["user_id"]
    user_name = request_data["user_name"]
    user_email = request_data["user_email"]
    user_phone = request_data["user_phone"]

    # Only get  retreat_id
    retreat_id = request_data["retreat_id"]

    payment_details = request_data["payment_details"]
    booking_date = request_data["booking_date"]

    booking = BookingsTable(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        retreat_id=retreat_id,
        payment_details=payment_details,
        booking_date=booking_date,
    )
    db.session.add(booking)

    try:
        db.session.commit()
    except exc.IntegrityError as integrityError:
        if isinstance(integrityError, exc.IntegrityError):
            return (
                jsonify(
                    {
                        "message": "User has already booked",
                    }
                ),
                # 409 Status code to indicate conflict
                409,
            )
    except Exception as otherError:
        return jsonify({"message": "Server error occurred"}), 500

    return jsonify({"message": "User has successfully booked"}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
