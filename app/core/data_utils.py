import re

def normalize_column(col: str) -> str:
    """
    Normalize column names into snake_case.

    Example:
    - "Total Sales ($)" → "total_sales"
    - "Order Date"      → "order_date"
    """
    col = col.strip().lower()
    col = re.sub(r"[^\w]+", "_", col)   # Replace non-alphanumeric with "_"
    col = re.sub(r"_+", "_", col)       # Collapse multiple "_"
    return col.strip("_")
