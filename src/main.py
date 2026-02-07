from config.settings import ASSET_CONFIG

from data.fetcher import fetch_daily_prices
from data.history_loader import load_historical_data
from data.merger import merge_historical_and_live

from processing.cleaner import clean_time_series
from model.forecaster import train_and_predict
from evaluation.metrics import calculate_error
from storage.local_store import save_result
from dashboard.app import show_dashboard
from dashboard.app import show_error_history


def main():
    print("System setup started")
    print("Assets to process:", list(ASSET_CONFIG.keys()))

    for asset_name, asset_info in ASSET_CONFIG.items():
        print("\n==============================")
        print(f"Processing asset: {asset_name}")
        print("==============================")

        # 1. Load historical data
        historical_df = load_historical_data(
            asset_name=asset_name,
            asset_config=asset_info
        )

        # 2. Fetch live price
        live_df = fetch_daily_prices(
            live_symbol=asset_info["live_symbol"]
        )

        # 3. Merge historical + live data
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

        # 7. Store result
        save_result(
            asset=asset_name,
            predicted_price=prediction,
            actual_price=actual_price,
            error=error
        )

        print(f"Prediction saved for {asset_name}")

    # 8. Show dashboard after all assets
    show_dashboard()
    show_error_history(last_n=10)
    
    print("\nSystem run completed")


if __name__ == "__main__":
    main()
