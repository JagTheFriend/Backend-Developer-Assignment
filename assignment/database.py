from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RetreatTable(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    date: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

    type: Mapped[str] = mapped_column()
    condition: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()

    tag: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()


class BookingsTable(db.Model):
    # Mark user Id has unique to make sure retreat cannot be double-booked for the same user.
    user_id: Mapped[int] = mapped_column(unique=True)
    user_name: Mapped[str] = mapped_column()
    user_email: Mapped[str] = mapped_column()
    user_phone: Mapped[int] = mapped_column()

    # Set retreat_id as the primary key
    retreat_id: Mapped[int] = mapped_column(primary_key=True)
    retreat_title: Mapped[str] = mapped_column()
    retreat_location: Mapped[str] = mapped_column()

    retreat_price: Mapped[int] = mapped_column()
    retreat_duration: Mapped[int] = mapped_column()

    payment_details: Mapped[str] = mapped_column()
    booking_date: Mapped[int] = mapped_column()
