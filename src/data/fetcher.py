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
    Returns DataFrame with columns: date, price
    """
    headers = {
        "X-Api-Key": API_KEY
    }

    params = {
        "name": live_symbol
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    # Debug visibility (important while learning)
    if response.status_code != 200:
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        response.raise_for_status()

    data = response.json()

    # API-Ninjas returns `updated` (not timestamp)
    df = pd.DataFrame([{
        "date": pd.to_datetime(data["updated"], unit="s"),
        "price": float(data["price"])
    }])

    print(f"Fetching live price for {live_symbol}...")
    return df
