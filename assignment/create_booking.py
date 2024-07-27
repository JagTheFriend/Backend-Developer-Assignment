from .database import BookingsTable, RetreatTable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult, and_


def create_booking(
    *,
    user_id: int,
    user_phone: int,
    retreat_id: int,
    booking_date: int,
    user_name: str,
    user_email: str,
    payment_details: str,
    db: SQLAlchemy,
):
    """
    Create a booking for a user for a retreat.

    Args:
        user_id (int): The ID of the user.
        user_phone (int): The phone number of the user.
        retreat_id (int): The ID of the retreat.
        booking_date (int): The date of the booking.
        user_name (str): The name of the user.
        user_email (str): The email of the user.
        payment_details (str): The details of the payment.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        dict: A dictionary with a message and a status code.
    """

    # Check if the user has already booked the retreat
    has_booked_retreat: ScalarResult[BookingsTable] | None = db.session.execute(
        db.select(BookingsTable).filter(
            and_(
                BookingsTable.user_id == user_id,
            )
        )
    ).scalar()

    if has_booked_retreat:
        return {"message": "User has already booked"}, 409

    # Check if the retreat exists
    retreat = db.session.execute(
        db.select(RetreatTable).filter(
            RetreatTable.id == retreat_id,
        )
    ).scalar()
    if not retreat:
        return {"message": "Invalid retreat ID"}, 404

    # Create a new booking
    booking = BookingsTable(
        user_id=user_id,
        user_phone=user_phone,
        retreat_id=retreat_id,
        booking_date=booking_date,
        user_name=user_name,
        user_email=user_email,
        payment_details=payment_details,
    )

    try:
        db.session.add(booking)
        db.session.commit()
        return {
            "message": "User has successfully booked",
            "booking_id": booking.id,
        }, 201
    except Exception as e:
        return {"message": "Server error occurred", "booking_id": "none"}, 201500
