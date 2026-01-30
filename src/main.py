from config.settings import COMMODITY_NAME
from data.fetcher import fetch_daily_prices
from processing.cleaner import clean_time_series
from model.forecaster import train_and_predict
from evaluation.metrics import calculate_error
from storage.local_store import save_result
from dashboard.app import show_dashboard


def main():
    print("System setup started")
    print("Commodity:", COMMODITY_NAME)

    # 1. Fetch data
    raw_df = fetch_daily_prices()

    # 2. Clean data
    clean_df = clean_time_series(raw_df)

    # 3. Predict
    prediction = train_and_predict(clean_df)

    # 4. Evaluate
    actual_price = clean_df["price"].iloc[-1]
    error = calculate_error(actual_price, prediction)

    # 5. Save result
    save_result(prediction, actual_price, error)
    print("Prediction saved")

    # 6. Show dashboard
    show_dashboard()


if __name__ == "__main__":
    main()
