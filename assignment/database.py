from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BookingsTable(db.Model):
    """
    BookingsTable represents the bookings made by users for retreats.
    It has a composite primary key consisting of user_id and retreat_id,
    ensuring that a user cannot double book the same retreat.\

    Attributes:
        user_name (Mapped[str]): The name of the user making the booking.
        user_email (Mapped[str]): The email of the user making the booking.
        user_phone (Mapped[int]): The phone number of the user making the booking.
        user_id (Mapped[int]): The unique ID of the user making the booking.
        retreat_id (Mapped[int]): The ID of the retreat being booked.
        retreat (relationship): The relationship to the RetreatTable model.
        payment_details (Mapped[str]): The details of the payment made for the booking.
        booking_date (Mapped[int]): The date when the retreat is booked.
    """

    user_name: Mapped[str] = mapped_column()
    user_email: Mapped[str] = mapped_column()
    user_phone: Mapped[int] = mapped_column()

    # Create a composite primary key so the user cannot double book the same retreat
    user_id: Mapped[int] = mapped_column()
    retreat_id: Mapped[int] = mapped_column(db.ForeignKey("retreat_table.id"))
    retreat = db.relationship("RetreatTable", backref="booking")

    payment_details: Mapped[str] = mapped_column()
    booking_date: Mapped[int] = mapped_column()

    __table_args__ = (
        db.PrimaryKeyConstraint(
            retreat_id,
            user_id,
        ),
    )


class RetreatTable(db.Model):
    """
    RetreatTable represents all the retreats offered by the platform.

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
