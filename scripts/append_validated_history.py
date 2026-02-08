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


def append_validated_history():
    print("Starting weekly validated history append...")

    for asset in ASSET_CONFIG.keys():
        print(f"\nProcessing asset: {asset}")

        # 1. Get latest date already in price_history
        history_resp = (
            supabase
            .table("price_history")
            .select("date")
            .eq("asset", asset)
            .order("date", desc=True)
            .limit(1)
            .execute()
        )

        last_history_date = None
        if history_resp.data:
            last_history_date = history_resp.data[0]["date"]

        # 2. Fetch validated actual prices from forecast_results
        query = (
            supabase
            .table("forecast_results")
            .select("date, actual_price")
            .eq("asset", asset)
        )

        if last_history_date:
            query = query.gt("date", last_history_date)

        results_resp = query.execute()

        if not results_resp.data:
            print("No new validated data to append.")
            continue

        # 3. Prepare rows for insertion
        rows = []
        for row in results_resp.data:
            rows.append({
                "date": row["date"],
                "asset": asset,
                "price": row["actual_price"],
                "source": "validated_forecast"
            })

        # 4. Insert into price_history
        supabase.table("price_history").insert(rows).execute()

        print(f"Appended {len(rows)} rows to price_history")

    print("\nWeekly append completed.")


if __name__ == "__main__":
    append_validated_history()
