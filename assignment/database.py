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
