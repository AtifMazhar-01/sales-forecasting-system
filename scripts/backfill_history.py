import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

from src.config.settings import ASSET_CONFIG

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

HISTORICAL_FILE = "data/commodity_futures.csv"


def backfill_history():
    print("Starting historical backfill...")

    df = pd.read_csv(HISTORICAL_FILE)

    # Normalize date column
    if "Date" in df.columns:
        df["date"] = pd.to_datetime(df["Date"])
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
    else:
        raise ValueError("No Date column found in historical CSV")

    for asset, asset_info in ASSET_CONFIG.items():
        print(f"\nBackfilling asset: {asset}")

        column = asset_info["historical_column"]

        if column not in df.columns:
            print(f"Column {column} not found, skipping.")
            continue

        asset_df = df[["date", column]].dropna()
        asset_df = asset_df.rename(columns={column: "price"})
        # Convert pandas Timestamp → string (JSON-safe)
        asset_df["date"] = asset_df["date"].dt.strftime("%Y-%m-%d")
        asset_df["asset"] = asset
        asset_df["source"] = "historical_csv"

        rows = asset_df.to_dict(orient="records")

        # Insert in batches to avoid limits
        batch_size = 500
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            supabase.table("price_history").insert(batch).execute()

        print(f"Inserted {len(rows)} rows for {asset}")

    print("\nHistorical backfill completed.")


if __name__ == "__main__":
    backfill_history()
