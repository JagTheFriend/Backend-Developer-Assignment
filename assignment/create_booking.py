from .database import BookingsTable
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult


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
    results: ScalarResult[BookingsTable] = db.session.execute(
        db.select(BookingsTable).filter(
            # The query searches for retreats where the condition or tags contain the filter
            BookingsTable.user_id
            == user_id,
        )
    ).scalars()

    # Check if the user has already booked the retreat
    has_user_booked_retreat = any(
        [booking.retreat_id == retreat_id for booking in results.all()]
    )

    if has_user_booked_retreat:
        return {"message": "User has already booked"}, 409

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
        return {"message": "User has successfully booked"}, 201
    except Exception:
        return {"message": "Server error occurred"}, 500
