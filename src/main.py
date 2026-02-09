import pandas as pd

from config.settings import ASSET_CONFIG

from data.fetcher import fetch_daily_prices
from data.cloud_history_loader import load_cloud_history
from data.merger import merge_historical_and_live

from processing.cleaner import clean_time_series
from model.forecaster import train_and_predict
from evaluation.metrics import calculate_error
from storage.cloud_store import save_result


def main():
    print("Using cloud storage for results")
    print("System setup started")
    print("Assets to process:", list(ASSET_CONFIG.keys()))

    for asset_name, asset_info in ASSET_CONFIG.items():
        print("\n==============================")
        print(f"Processing asset: {asset_name}")
        print("==============================")

        # 1. Load historical data from cloud (Supabase)
        historical_df = load_cloud_history(asset_name)

        # 2. Fetch live price
        live_df = fetch_daily_prices(
            live_symbol=asset_info["live_symbol"]
        )

        # 2.a FALLBACK if API is blocked / premium-only
        if live_df is None:
            print(f"[INFO] Using fallback price for {asset_name}")

            live_df = historical_df.tail(1)[["date", "price"]].copy()
            live_df["date"] = (
                pd.to_datetime(live_df["date"]) + pd.Timedelta(days=1)
            )

        # 3. Merge historical + live
        combined_df = merge_historical_and_live(
            historical_df,
            live_df
        )

        # 4. Clean data
        clean_df = clean_time_series(combined_df)

        # 5. Train & predict
        prediction = train_and_predict(clean_df)

        # 6. Evaluate
        actual_price = clean_df["price"].iloc[-1]
        error = calculate_error(actual_price, prediction)

        # 7. Store result in Supabase
        save_result(
            asset=asset_name,
            predicted_price=prediction,
            actual_price=actual_price,
            error=error
        )

        print(f"Prediction saved for {asset_name}")

    print("\nSystem run completed")


if __name__ == "__main__":
    main()
