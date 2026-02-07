import pandas as pd
from prophet import Prophet


def train_and_predict(df):
    """
    Prophet-based time series forecasting model
    Predicts next day's price
    """

    # Prophet expects columns: ds (date), y (value)
    prophet_df = df.rename(
        columns={
            "date": "ds",
            "price": "y"
        }
    )[["ds", "y"]]

    # Initialize Prophet
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    # Train model
    model.fit(prophet_df)

    # Create future dataframe (1 day ahead)
    future = model.make_future_dataframe(periods=1)

    forecast = model.predict(future)

    # Get tomorrow's prediction
    prediction = forecast.iloc[-1]["yhat"]

    return float(prediction)
