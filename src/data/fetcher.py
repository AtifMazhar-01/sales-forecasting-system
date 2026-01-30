import requests
import pandas as pd
from datetime import datetime

def fetch_daily_prices():
    """
    Fetch daily commodity prices from API
    (placeholder – real API logic comes next step)
    """
    print("Fetching daily prices...")

    # Dummy data for now (structure only)
    data = {
        "date": [datetime.today().strftime("%Y-%m-%d")],
        "price": [100.0]
    }

    df = pd.DataFrame(data)
    return df

