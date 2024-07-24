from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult
from database import RetreatTable
from json import loads


def filter_by_tag(filter_: str, db: SQLAlchemy):
    data: list[RetreatTable] = []

    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable)
        # In this case, we'll only take condition while filtering
        .filter(RetreatTable.condition.icontains(f"%{filter_}%")).order_by(
            RetreatTable.id
        )
    ).scalars()

    for result in results.all():
        data.append(
            {
                "id": result.id,
                "title": result.title,
                "description": result.description,
                "condition": result.condition,
                "location": result.location,
                "date": result.date,
                "price": result.price,
                "image": result.image,
                "tags": loads(result.tags),
            }
        )
    return data


def filter_by_location(location: str, db: SQLAlchemy):
    retreats = (
        db.session.query(RetreatTable)
        .filter(RetreatTable.location.ilike(f"%{location}%"))
        .all()
    )
    return retreats


def filter_by_search(search: str, db: SQLAlchemy):
    retreats = (
        db.session.query(RetreatTable)
        .filter(RetreatTable.title.ilike(f"%{search}%"))
        .all()
    )
    return retreats


def pagination(page_number: int, limit: int, db: SQLAlchemy):
    pass
