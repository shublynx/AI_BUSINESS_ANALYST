import re

SYNONYMS = {
    "sales": ["amount", "revenue", "value"],
    "qty": ["quantity", "units", "count"],
    "price": ["cost", "rate"],
}

def normalize(text: str) -> set:
    text = re.sub(r"[^a-zA-Z0-9_ ]", "", text.lower())
    return set(text.replace("_", " ").split())

def expand(tokens: set) -> set:
    expanded = set(tokens)
    for token in tokens:
        for key, values in SYNONYMS.items():
            if token == key or token in values:
                expanded.update([key] + values)
    return expanded

def match_column(metadata: dict, question: str) -> str:
    question_tokens = expand(normalize(question))

    best_score = -1
    best_column = None

    for col in metadata["columns"]:
        col_tokens = expand(normalize(col["name"]))

        score = len(question_tokens & col_tokens)

        # numeric columns are better aggregation targets
        if col["dtype"].startswith(("int", "float")):
            score += 1

        if score > best_score:
            best_score = score
            best_column = col["name"]

    return best_column
