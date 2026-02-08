
import os
from datetime import date
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env file (local dev)
load_dotenv()

# Load credentials from environment (GitHub Secrets / local env)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials not found in environment variables")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_result(asset, predicted_price, actual_price, error):
    """
    Save daily forecast result to Supabase (forecast_results table)
    """

    payload = {
        "date": date.today().isoformat(),
        "asset": asset,
        "predicted_price": float(predicted_price),
        "actual_price": float(actual_price),
        "error": float(error)
    }

    response = (
        supabase
        .table("forecast_results")
        .insert(payload)
        .execute()
    )

    # Defensive check (optional, safe)
    if response.data is None:
        raise RuntimeError("Insert failed: no data returned from Supabase")
