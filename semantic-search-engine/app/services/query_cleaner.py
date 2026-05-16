import re


def clean_query(query: str) -> str:
    query = query.strip().lower()
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r'[^\w\s]', '', query)
    return query
