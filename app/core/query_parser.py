AGG_KEYWORDS = {
    "sum": ["total", "sum"],
    "avg": ["average", "mean"],
    "max": ["highest", "max"],
    "min": ["lowest", "min"],
    "count": ["count", "how many"],
}

def parse_question(question: str) -> dict:
    q = question.lower()

    aggregation = None
    for agg, words in AGG_KEYWORDS.items():
        if any(w in q for w in words):
            aggregation = agg
            break

    return {
        "aggregation": aggregation,
        "raw": q,
    }
