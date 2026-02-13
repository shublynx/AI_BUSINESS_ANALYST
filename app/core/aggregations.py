def run_aggregation(df, aggregation, metric_col, group_by=None):
    if group_by:
        if aggregation == "sum":
            return df.groupby(group_by)[metric_col].sum()
        if aggregation == "avg":
            return df.groupby(group_by)[metric_col].mean()
        if aggregation == "max":
            return df.groupby(group_by)[metric_col].max()
        if aggregation == "min":
            return df.groupby(group_by)[metric_col].min()
        if aggregation == "count":
            return df.groupby(group_by)[metric_col].count()
    else:
        if aggregation == "sum":
            return df[metric_col].sum()
        if aggregation == "avg":
            return df[metric_col].mean()
        if aggregation == "max":
            return df[metric_col].max()
        if aggregation == "min":
            return df[metric_col].min()
        if aggregation == "count":
            return df[metric_col].count()
