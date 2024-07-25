from flask import Flask, request, jsonify
from filters import (
    filter_by_location,
    filter_by_search,
    filter_by_tag,
    get_all_retreats,
    pagination,
)
from database import db, BookingsTable
from sqlalchemy import exc
from waitress import serve

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/retreats", methods=["GET"])
def get_retreats():
    filter_ = request.args.get("filter")
    if filter_:
        data = filter_by_tag(filter_, db)
        return jsonify(data), 201

    location = request.args.get("location")
    if location:
        data = filter_by_location(location, db)
        return jsonify(data), 201

    search = request.args.get("search")
    if search:
        data = filter_by_search(search, db)
        return jsonify(data), 201

    page_number = request.args.get("page")
    if page_number:
        received_limit = request.args.get("limit")
        data = pagination(page_number, received_limit, db)
        return jsonify(data), 201

    return get_all_retreats(db)


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
        # Converted the relevant fields to int
        user_id=int(user_id),
        user_phone=int(user_phone),
        retreat_id=int(retreat_id),
        booking_date=int(booking_date),
        user_name=user_name,
        user_email=user_email,
        payment_details=payment_details,
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
    # app.run(debug=True)
    serve(app, host="0.0.0.0", port=5000)
