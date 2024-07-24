from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult
from util import extract_query_content
from database import RetreatTable


def filter_by_tag(filter_: str, db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable)
        .filter(
            or_(
                RetreatTable.condition.icontains(f"%{filter_}%"),
                RetreatTable.tags.icontains(f"%{filter_}%"),
            )
        )
        .order_by(RetreatTable.id)
    ).scalars()
    return extract_query_content(results.all())


def filter_by_location(location: str, db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.location.icontains(f"%{location}%"))
    ).scalars()
    return extract_query_content(results.all())


def filter_by_search(search: str, db: SQLAlchemy):
    retreats = (
        db.session.query(RetreatTable)
        .filter(RetreatTable.title.ilike(f"%{search}%"))
        .all()
    )
    return retreats


def pagination(page_number: int, limit: int, db: SQLAlchemy):
    pass
