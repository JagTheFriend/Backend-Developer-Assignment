from typing import Sequence
from database import RetreatTable
from json import loads


def extract_query_results(query_results: Sequence[RetreatTable]) -> list[dict]:
    """
    Extracts the relevant information from the query results and returns a list of extracted data.s

    Args:
        query_results (Sequence[RetreatTable]): The results of a SQL query.

    Returns:
        list[dict]: A list of dictionaries containing the extracted information.
    """
    extracted_data: list[dict] = []
    for result in query_results:
        extracted_data.append(
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
    return extracted_data
