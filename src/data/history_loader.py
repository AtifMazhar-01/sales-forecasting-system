import pandas as pd


def load_historical_data(asset_name, asset_config, filepath="data/commodity_futures.csv"):
    """
    Load historical prices for a specific asset.
    Returns DataFrame with columns: date, price
    """
    df = pd.read_csv(filepath)

    # --- Detect date column safely ---
    possible_date_cols = ["date", "Date", "DATE"]

    date_col = None
    for col in possible_date_cols:
        if col in df.columns:
            date_col = col
            break

    if date_col is None:
        raise ValueError("No date column found in historical CSV")

    df[date_col] = pd.to_datetime(df[date_col])

    # --- Get correct commodity column ---
    column_name = asset_config["historical_column"]

    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in historical data")

    asset_df = df[[date_col, column_name]].copy()
    asset_df.rename(
        columns={
            date_col: "date",
            column_name: "price"
        },
        inplace=True
    )

    # Safety: ensure correct time order
    asset_df = asset_df.sort_values("date").reset_index(drop=True)

    return asset_df
