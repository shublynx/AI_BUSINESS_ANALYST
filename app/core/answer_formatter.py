def format_aggregation(result):
    if hasattr(result, "idxmax"):
        idx = result.idxmax()
        value = result.loc[idx]
        return f"{idx} has the highest value: {value}"

    return f"Result: {result}"
