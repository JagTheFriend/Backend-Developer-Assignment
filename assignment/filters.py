from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult, or_
from util import extract_query_content
from database import RetreatTable


def filter_by_tag(filter_: str, db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(
            or_(
                RetreatTable.condition.icontains(f"%{filter_}%"),
                RetreatTable.tags.icontains(f"%{filter_}%"),
            )
        )
    ).scalars()
    return extract_query_content(results.all())


def filter_by_location(location: str, db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.location.icontains(f"%{location}%"))
    ).scalars()
    return extract_query_content(results.all())


def filter_by_search(search: str, db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(
            or_(
                RetreatTable.title.icontains(f"%{search}%"),
                RetreatTable.condition.icontains(f"%{search}%"),
                RetreatTable.tags.icontains(f"%{search}%"),
            )
        )
    ).scalars()
    return extract_query_content(results.all())


def pagination(page_number: str, limit: str, db: SQLAlchemy):
    # Convert page number and limit to integers
    page_number = (
        int(page_number)
        if page_number.isnumeric() and int(page_number) > 0
        else 1  # default to first page
    )
    limit = (
        int(limit)
        if limit is not None and limit.isnumeric() and int(limit) > 0
        else 2  # default to 2 results per page
    )

    results: ScalarResult[RetreatTable] = (
        db.session.query(RetreatTable)
        .order_by(RetreatTable.id)
        .offset((page_number - 1) * limit)
        .limit(limit)
        .all()
    )
    return extract_query_content(results)


def get_all_retreats(db: SQLAlchemy):
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter()
    ).scalars()
    return extract_query_content(results.all())
