from flask import Flask, request, jsonify
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
    received_filter = request.args.get("filter")
    if received_filter:
        return

    received_location = request.args.get("location")
    if received_location:
        return

    received_limit = request.args.get("limit")
    if received_limit:
        return

    page_number = request.args.get("page")
    # Set limit to -1 if page number is not provided
    received_limit = request.args.get("limit") or -1
    if page_number:
        return

    return {"data": []}


@app.route("/retreats/book", methods=["POST"])
def book_retreat():
    """
    Endpoint for booking a retreat.

    This endpoint expects a JSON payload with the following fields:
    - user_id: ID of the user booking the retreat.
    - user_name: Name of the user booking the retreat.
    - user_email: Email of the user booking the retreat.
    - user_phone: Phone number of the user booking the retreat.
    - retreat_id: ID of the retreat being booked.
    - payment_details: Details of the payment made for the retreat booking.
    - booking_date: Date when the retreat is booked.

    Returns a JSON response with a message indicating the success or failure of the booking.
    If the booking is successful, the response has a status code of 201.
    If the user has already booked the retreat, the response has a status code of 409.
    If the server encounters any other error, the response has a status code of 500.
    """
    data = request.get_json()

    # Extract data from request payload
    retreat_id = data["retreat_id"]

    payment_details = data["payment_details"]
    booking_date = data["booking_date"]

    user_id = data["user_id"]
    user_name = data["user_name"]
    user_email = data["user_email"]
    user_phone = data["user_phone"]

    booking = BookingsTable(
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        retreat_id=retreat_id,
        payment_details=payment_details,
        booking_date=booking_date,
    )

    try:
        # Add the booking to the database
        db.session.add(booking)
        db.session.commit()
        return jsonify({"message": "User has successfully booked"}), 201

    # If the user has already booked the retreat, return a 409 error
    except exc.IntegrityError:
        return jsonify({"message": "User has already booked"}), 409

    # If any other error occurs, return a 500 error
    except Exception:
        return jsonify({"message": "Server error occurred"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
