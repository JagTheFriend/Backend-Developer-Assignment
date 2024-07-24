from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BookingsTable(db.Model):
    """
    Attributes:
        booking_id (int): The unique ID of the booking.
        user_id (int): The ID of the user who made the booking. This is marked as unique to
            make sure that a retreat cannot be double-booked for the same user.
        user_name (str): The name of the user who made the booking.
        user_email (str): The email of the user who made the booking.
        user_phone (int): The phone number of the user who made the booking.
        retreat_id (int): The ID of the retreat that was booked. This is set as the primary key.
        retreat (RetreatTable): A relationship to the RetreatTable model that represents the retreat
            that was booked.
        payment_details (str): The details of the payment made for the booking.
        booking_date (int): The date of the booking.
    """

    id: Mapped[int] = mapped_column(primary_key=True)

    # Mark user Id as unique to make sure retreat cannot be double-booked for the same user.
    user_id: Mapped[int] = mapped_column(unique=True)
    user_name: Mapped[str] = mapped_column()
    user_email: Mapped[str] = mapped_column()
    user_phone: Mapped[int] = mapped_column()

    # Set retreat_id as the primary key
    retreat_id: Mapped[int] = mapped_column(db.ForeignKey("retreat_table.id"))
    retreat = db.relationship("RetreatTable", backref="booking")

    payment_details: Mapped[str] = mapped_column()
    booking_date: Mapped[int] = mapped_column()


class RetreatTable(db.Model):
    """
    Attributes:
        id (int): The unique ID of the retreat.
        title (str): The title of the retreat.
        description (str): The description of the retreat.
        date (int): The date of the retreat.
        location (str): The location of the retreat.
        price (int): The price of the retreat.
        type (str): The type of the retreat.
        condition (str): The condition of the retreat.
        image (str): The image of the retreat.
        tags (str): The tags of the retreat.
        duration (int): The duration of the retreat.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    date: Mapped[int] = mapped_column()
    location: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()

    type: Mapped[str] = mapped_column()
    condition: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()

    duration: Mapped[int] = mapped_column()

    # Save a list of tags by json.dumps(["tag1", "tag2"])
    # Load a list of tags by json.loads(tags)
    tags: Mapped[str] = mapped_column()
