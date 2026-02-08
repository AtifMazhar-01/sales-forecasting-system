import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_cloud_history(asset):
    """
    Load full historical time series for a single asset
    from Supabase price_history table.

    Returns DataFrame with columns: date, price
    """

    response = (
        supabase
        .table("price_history")
        .select("date, price")
        .eq("asset", asset)
        .order("date")
        .execute()
    )

    if not response.data:
        raise ValueError(f"No history found for asset: {asset}")

    df = pd.DataFrame(response.data)
    df["date"] = pd.to_datetime(df["date"])

    return df
