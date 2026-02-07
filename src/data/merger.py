import pandas as pd


def merge_historical_and_live(historical_df, live_df):
    """
    Append live price to historical data if date is new.
    Returns combined DataFrame with columns: date, price
    """
    # Ensure correct types
    historical_df["date"] = pd.to_datetime(historical_df["date"])
    live_df["date"] = pd.to_datetime(live_df["date"])

    # If live date already exists, do NOT duplicate
    if live_df["date"].iloc[0] in historical_df["date"].values:
        combined_df = historical_df.copy()
    else:
        combined_df = pd.concat(
            [historical_df, live_df],
            ignore_index=True
        )

    # Sort by date (important for time series)
    combined_df = combined_df.sort_values("date").reset_index(drop=True)

    return combined_df
