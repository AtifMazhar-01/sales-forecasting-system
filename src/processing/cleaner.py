import pandas as pd

def clean_time_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare time-series data for modeling
    """
    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"])

    # Sort by date
    df = df.sort_values("date")

    # Reset index
    df = df.reset_index(drop=True)

    return df
