import pandas as pd
import os
from datetime import date

RESULTS_FILE = "data/results.csv"


def save_result(asset, predicted_price, actual_price, error):
    today = date.today()

    new_row = {
        "date": today,
        "asset": asset,
        "predicted_price": predicted_price,
        "actual_price": actual_price,
        "error": error
    }

    if os.path.exists(RESULTS_FILE):
        df = pd.read_csv(RESULTS_FILE)
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # Remove existing record for same date & asset
        df = df[
            ~((df["date"] == today) & (df["asset"] == asset))
        ]

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])
    df = df.sort_values(["date", "asset"])


    df.to_csv(RESULTS_FILE, index=False)
