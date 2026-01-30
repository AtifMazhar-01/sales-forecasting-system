import pandas as pd

def show_dashboard():
    """
    Simple dashboard to display prediction history
    """
    try:
        df = pd.read_csv("results.csv")
        print("\n=== Prediction History ===")
        print(df.tail())
    except FileNotFoundError:
        print("No results found yet.")
