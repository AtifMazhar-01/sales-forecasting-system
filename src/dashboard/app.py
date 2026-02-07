import pandas as pd
import os


RESULTS_FILE = "data/results.csv"


def show_dashboard():
    if not os.path.exists(RESULTS_FILE):
        print("No results found yet.")
        return

    df = pd.read_csv(RESULTS_FILE)

    if df.empty:
        print("Results file is empty.")
        return

    # Ensure date is treated correctly
    df["date"] = pd.to_datetime(df["date"])

    # Get latest date
    latest_date = df["date"].max()

    # Filter latest results only
    latest_df = df[df["date"] == latest_date].copy()

    # Sort for readability
    latest_df = latest_df.sort_values("asset")

    print("\n=== Latest Prediction Snapshot ===")
    print(f"Date: {latest_date.date()}\n")

    print(
        latest_df[
            ["asset", "predicted_price", "actual_price", "error"]
        ].to_string(index=False)
    )

def show_error_history(asset=None, last_n=10):
    """
    Show error trend over time.
    If asset is None, show all assets.
    """
    if not os.path.exists(RESULTS_FILE):
        print("No results found yet.")
        return

    df = pd.read_csv(RESULTS_FILE)
    df["date"] = pd.to_datetime(df["date"])

    if asset:
        df = df[df["asset"] == asset]

    df = df.sort_values("date").tail(last_n)

    print("\n=== Error History ===")
    if asset:
        print(f"Asset: {asset}")
    print(df[["date", "asset", "error"]].to_string(index=False))

