import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_NINJAS_KEY")
BASE_URL = "https://api.api-ninjas.com/v1/commodityprice"


def fetch_daily_prices(live_symbol):
    """
    Fetch latest price for a given commodity symbol from API-Ninjas.

    Returns:
        pd.DataFrame with columns: date, price
        OR
        None (if API fails / asset not available)
    """

    headers = {
        "X-Api-Key": API_KEY
    }

    params = {
        "name": live_symbol
    }

    print(f"Fetching live price for {live_symbol}...")

    response = requests.get(BASE_URL, headers=headers, params=params)

    # ---- HARD SAFETY (DO NOT BREAK PIPELINE) ----
    if response.status_code != 200:
        print(f"[WARN] Live price fetch failed for {live_symbol}")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None   #  CRITICAL: do NOT raise exception

    data = response.json()

    # API-Ninjas returns `updated` as UNIX timestamp
    df = pd.DataFrame([{
        "date": pd.to_datetime(data["updated"], unit="s"),
        "price": float(data["price"])
    }])

    return df
