from flask import Flask, request, jsonify
from sqlalchemy.sql.functions import user
from .filters import (
    filter_by_duration,
    filter_by_location,
    filter_by_title,
    filter_by_search,
    filter_by_tag,
    filter_by_type,
    get_all_retreats,
    pagination,
)
from .database import db, BookingsTable
from .create_booking import create_booking
from waitress import serve

import time
import os
import logging

# Added logging
logger = logging.getLogger("waitress")
logger.setLevel(logging.INFO)

app = Flask(__name__)
# Get the database URL from the environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
# "sqlite:///project.db"

db.init_app(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/retreats", methods=["GET"])
def get_retreats():
    filter_ = request.args.get("filter")
    if filter_:
        data = filter_by_tag(filter_, db)
        return jsonify(data), 200

    title = request.args.get("title")
    if title:
        data = filter_by_title(title, db)
        return jsonify(data), 200

    duration = request.args.get("duration")
    if duration:
        data = filter_by_duration(duration, db)
        return jsonify(data), 200

    type_ = request.args.get("type")
    if type_:
        data = filter_by_type(type_, db)
        return jsonify(data), 200

    location = request.args.get("location")
    if location:
        data = filter_by_location(location, db)
        return jsonify(data), 200

    search = request.args.get("search")
    if search:
        data = filter_by_search(search, db)
        return jsonify(data), 200

    page_number = request.args.get("page")
    if page_number:
        received_limit = request.args.get("limit")
        data = pagination(page_number, received_limit, db)
        return jsonify(data), 200

    return get_all_retreats(db), 200


@app.route("/book/delete", methods=["DELETE"])
def delete_booking():
    """
    Endpoint for deleting a booking.
    """
    booking_id = request.args.get("id")

    if not booking_id:
        return jsonify({"message": "Missing booking ID"}), 400

    if not booking_id.isnumeric():
        return jsonify({"message": "Invalid booking ID"}), 400

    try:
        db.session.query(BookingsTable).filter_by(id=int(booking_id)).delete()
        db.session.commit()
        return jsonify({"message": "Booking deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Server error occurred"}), 500


@app.route("/book", methods=["POST"])
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

    required_fields = [
        # User details
        "user_id",
        "user_name",
        "user_email",
        "user_phone",
        # Retreat details
        "retreat_title",
        "retreat_location",
        "retreat_price",
        "retreat_duration",
        "retreat_id",
        # Payment details
        "payment_details",
        "booking_date",
    ]
    missing_fields = any([field not in data for field in required_fields])

    if missing_fields:
        return jsonify({"message": f"Missing data"}), 400

    retreat_id = data["retreat_id"]
    payment_details = data["payment_details"]
    booking_date = data["booking_date"]

    user_id = data["user_id"]
    user_name = data["user_name"]
    user_email = data["user_email"]
    user_phone: str = data["user_phone"]

    # Check if the fields are the correct type
    if not all(
        [
            val.isnumeric()
            for val in [
                user_id,
                user_phone,
                retreat_id,
                booking_date,
            ]
        ]
    ):
        return jsonify({"message": "Invalid type"}), 400

    result, status_code = create_booking(
        user_id=int(user_id),
        user_phone=int(user_phone),
        retreat_id=int(retreat_id),
        booking_date=int(booking_date),
        user_name=user_name,
        user_email=user_email,
        payment_details=payment_details,
        db=db,
    )
    return jsonify(result), status_code


def start_server():
    with app.app_context():
        # Used try-catch here since it may take few seconds
        # for the database to be ready to accept connections
        # when running this application through docker compose
        while True:
            try:
                db.create_all()
            except Exception:
                # Try to reconnect every 3 seconds
                time.sleep(3)
            else:
                break

    # app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
