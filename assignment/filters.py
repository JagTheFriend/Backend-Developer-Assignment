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
                "location": result.location,
                "duration": result.duration,
                "date": result.date,
                "price": result.price,
                "type": result.type,
                "condition": result.condition,
                "image": result.image,
                "tags": loads(result.tags),
            }
        )
    return data


def filter_by_location(location: str, db: SQLAlchemy):
    data: list[RetreatTable] = []

    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable)
        # In this case, we'll only take condition while filtering
        .filter(RetreatTable.location.icontains(f"%{location}%")).order_by(
            RetreatTable.id
        )
    ).scalars()

    for result in results.all():
        data.append(
            {
                "title": result.title,
                "description": result.description,
                "date": result.date,
                "location": result.location,
                "price": result.price,
                "type": result.type,
                "condition": result.condition,
                "image": result.image,
                "tags": loads(result.tags),
                "duration": result.duration,
                "id": result.id,
            }
        )
    return data


def filter_by_search(search: str, db: SQLAlchemy):
    retreats = (
        db.session.query(RetreatTable)
        .filter(RetreatTable.title.ilike(f"%{search}%"))
        .all()
    )
    return retreats


def pagination(page_number: int, limit: int, db: SQLAlchemy):
    pass
