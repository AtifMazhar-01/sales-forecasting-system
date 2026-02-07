import os
import pandas as pd

from src.config.settings import ASSET_CONFIG
from src.data.history_loader import load_historical_data

RESULTS_FILE = "data/results.csv"


def append_validated_history():
    # safe exit if no results yet
    if not os.path.exists(RESULTS_FILE):
        print("No results.csv found. Skipping history append.")
        return

    print("Starting batch history append...")

    results_df = pd.read_csv(RESULTS_FILE)
    results_df["date"] = pd.to_datetime(results_df["date"])

    for asset_name, asset_info in ASSET_CONFIG.items():
        print(f"\nProcessing asset: {asset_name}")

        # Load existing historical data
        hist_df = load_historical_data(asset_name, asset_info)
        last_hist_date = hist_df["date"].max()

        # Filter validated actuals
        asset_actuals = results_df[
            (results_df["asset"] == asset_name) &
            (results_df["date"] > last_hist_date)
        ][["date", "actual_price"]]

        if asset_actuals.empty:
            print("No new validated data to append.")
            continue

        # Rename to match historical format
        asset_actuals = asset_actuals.rename(
            columns={"actual_price": "price"}
        )

        # Append and sort
        updated_hist = pd.concat(
            [hist_df, asset_actuals],
            ignore_index=True
        ).sort_values("date")

        # Save per-asset history (safe approach)
        output_file = f"data/history_{asset_name}.csv"
        updated_hist.to_csv(output_file, index=False)

        print(f"Updated history saved to {output_file}")

    print("\nBatch append completed.")


if __name__ == "__main__":
    append_validated_history()
