from typing import Sequence
from assignment.database import RetreatTable
from json import loads


def extract_query_content(results: Sequence[RetreatTable]):
    data: list[RetreatTable] = []
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
