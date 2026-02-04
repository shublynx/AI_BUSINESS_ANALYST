import pandas as pd


def extract_metadata(df: pd.DataFrame) -> dict:
    """
    Extract lightweight, structured metadata from a dataset.

    This metadata is:
    - small enough to store in DB
    - rich enough for analytics & LLM grounding
    """

    return {
        "row_count": int(df.shape[0]),      # Total number of rows
        "column_count": int(df.shape[1]),   # Total number of columns

        "columns": [
            {
                "name": col,                               # Normalized column name
                "dtype": str(df[col].dtype),               # Pandas inferred type
                "nulls": int(df[col].isna().sum()),         # Missing values count
                "unique": int(df[col].nunique()),           # Distinct values count
            }
            for col in df.columns
        ],
    }
