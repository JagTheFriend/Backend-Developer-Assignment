from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ScalarResult, or_
from util import extract_query_results
from database import RetreatTable


def filter_by_tag(filter_: str, db: SQLAlchemy):
    """
    Filter retreats by tag or condition.

    Args:
        filter_ (str): The tag or condition to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the filter.
    """
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(
            or_(
                # The query searches for retreats where the condition or tags contain the filter
                RetreatTable.condition.icontains(f"%{filter_}%"),
                RetreatTable.tags.icontains(f"%{filter_}%"),
            )
        )
    ).scalars()
    return extract_query_results(results.all())


def filter_by_title(title: str, db: SQLAlchemy):
    """
    Filter retreats by title.

    Args:
        title (str): The title to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the title.
    """
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.title.icontains(f"%{title}%"))
    ).scalars()
    return extract_query_results(results.all())


def filter_by_location(location: str, db: SQLAlchemy):
    """
    Filter retreats by location.

    Args:
        location (str): The location to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the location.
    """
    # Query the database for retreats where the location contains the filter
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.location.icontains(f"%{location}%"))
    ).scalars()
    return extract_query_results(results.all())


def filter_by_type(type_: str, db: SQLAlchemy):
    """
    Filter retreats by type.

    Args:
        type_ (str): The type to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the type.
    """
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.type.icontains(f"%{type_}%"))
    ).scalars()
    return extract_query_results(results.all())


def filter_by_duration(duration: str, db: SQLAlchemy):
    """
    Filter retreats by duration.

    Args:
        duration (str): The duration to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the duration.
    """
    # If duration is not a number, set it to 5 (default duration)
    duration = duration if duration.isnumeric() else "5"

    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(RetreatTable.duration.icontains(f"%{duration}%"))
    ).scalars()
    return extract_query_results(results.all())


def filter_by_search(search: str, db: SQLAlchemy):
    """
    Filter retreats by search term.

    Args:
        search (str): The search term to filter by.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the search term.
    """
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable).filter(
            # Query the database for retreats where the title, condition, or tags contain the search term
            or_(
                RetreatTable.title.icontains(f"%{search}%"),
                RetreatTable.condition.icontains(f"%{search}%"),
                RetreatTable.tags.icontains(f"%{search}%"),
            )
        )
    ).scalars()
    return extract_query_results(results.all())


def pagination(page_number: str, limit: str | None, db: SQLAlchemy) -> list[dict]:
    """
    Paginate the results of a query.

    Args:
        page_number (str): The page number to return.
        limit (str | None): The number of results per page.
        db (SQLAlchemy): The SQLAlchemy database object.

    Returns:
        list[dict]: A list of retreats that match the pagination criteria.
    """
    # Convert page number and limit to integers
    current_page_number = (
        int(page_number)
        if page_number.isnumeric() and int(page_number) > 0
        else 1  # default to first page
    )
    current_limit = (
        int(limit)
        if limit is not None and limit.isnumeric() and int(limit) > 0
        else 2  # default to 2 results per page
    )

    results: list[RetreatTable] = (
        db.session.query(RetreatTable)
        .order_by(RetreatTable.id)
        .offset((current_page_number - 1) * current_limit)
        .limit(current_limit)
        .all()
    )
    return extract_query_results(results)


def get_all_retreats(db: SQLAlchemy) -> list[dict]:
    """
    Retrieves all retreats from the database.

    Args:
        db (SQLAlchemy): An instance of SQLAlchemy.

    Returns:
        list[dict]: A list of dictionaries containing the retreat data.
    """
    results: ScalarResult[RetreatTable] = db.session.execute(
        db.select(RetreatTable)
    ).scalars()
    return extract_query_results(results.all())
