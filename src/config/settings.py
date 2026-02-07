
# Global Project Settings


# Data frequency
DATA_FREQUENCY = "daily"

# Prediction setup
PREDICTION_HORIZON = 1  # one-step ahead (tomorrow)

# Model config (baseline for now)
MODEL_NAME = "time_series_baseline"

# Asset Configuration

# This is the SINGLE source of truth
# for all commodities in the system

ASSET_CONFIG = {
    "GOLD": {
        "historical_column": "GOLD",
        "live_symbol": "micro_gold"
    },
    "SILVER": {
        "historical_column": "SILVER",
        "live_symbol": "micro_silver"
    },
    "NATURAL_GAS": {
        "historical_column": "NATURAL GAS",
        "live_symbol": "natural_gas"
    },
    "LIVE_CATTLE": {
        "historical_column": "LIVE CATTLE",
        "live_symbol": "live_cattle"
    }
}
