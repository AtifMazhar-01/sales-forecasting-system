import pandas as pd
from datetime import datetime
import os

def save_result(predicted: float, actual: float, error: float):
    """
    Save daily prediction result locally
    """
    file_path = "results.csv"

    data = {
        "date": [datetime.today().strftime("%Y-%m-%d")],
        "predicted_price": [predicted],
        "actual_price": [actual],
        "error": [error]
    }

    df = pd.DataFrame(data)

    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
