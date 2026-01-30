import pandas as pd

def train_and_predict(df: pd.DataFrame) -> float:
    """
    Simple baseline time-series model:
    Predict tomorrow's price using last known value
    (placeholder for advanced model later)
    """
    # Last observed price
    last_price = df["price"].iloc[-1]

    # One-step-ahead prediction
    predicted_price = last_price

    return float(predicted_price)
