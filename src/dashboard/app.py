import streamlit as st
import pandas as pd
import plotly.express as px
import os
from supabase import create_client
from dotenv import load_dotenv
from datetime import timedelta

# ================== CONFIG ==================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials not found")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Commodity Forecast Dashboard",
    layout="wide"
)

st.title("📊 Commodity Forecast Dashboard")
st.caption("Historical prices, daily forecasts, and error analysis")

# ================== DATA LOADERS ==================
@st.cache_data(ttl=300)
def load_forecast_results():
    res = (
        supabase
        .table("forecast_results")
        .select("*")
        .order("date", desc=False)
        .execute()
    )
    df = pd.DataFrame(res.data)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
    return df


@st.cache_data(ttl=300)
def load_price_history():
    all_rows = []
    batch_size = 1000
    start = 0

    while True:
        res = (
            supabase
            .table("price_history")
            .select("date, asset, price")
            .range(start, start + batch_size - 1)
            .execute()
        )

        if not res.data:
            break

        all_rows.extend(res.data)

        if len(res.data) < batch_size:
            break

        start += batch_size

    df = pd.DataFrame(all_rows)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    return df



forecast_df = load_forecast_results()
history_df = load_price_history()


if forecast_df.empty or history_df.empty:
    st.warning("Data not available yet.")
    st.stop()

# ================== HELPERS ==================
RANGE_MAP = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
    "5 Years": 365 * 5,
    "10 Years": 365 * 10,
    "20 Years": 365 * 20,
    "All Available": None,
}

def apply_history_range(df: pd.DataFrame, days: int | None):
    if days is None:
        return df.sort_values("date")
    
    
    from datetime import datetime
    latest_date = df["date"].max()
    cutoff_date = latest_date - timedelta(days=days)
    
    filtered = df[df["date"] >= cutoff_date].copy()
    return filtered.sort_values("date")


assets = sorted(history_df["asset"].unique())

# ================== SIDEBAR ==================
st.sidebar.header("Controls")

mode = st.sidebar.radio(
    "View Mode",
    ["Single Asset", "Multi Asset"],
)

# ==================================================
# SINGLE ASSET MODE (TABLE INCLUDED)
# ==================================================
if mode == "Single Asset":
    asset = st.sidebar.selectbox("Select Asset", assets)

    asset_forecast = (
        forecast_df[forecast_df["asset"] == asset]
        .sort_values("date")
        .reset_index(drop=True)
    )

    selected_date = st.sidebar.selectbox(
        "Select Forecast Date",
        asset_forecast["date"].dt.date.unique()[::-1],
    )

    row = asset_forecast[
        asset_forecast["date"].dt.date == selected_date
    ].iloc[0]

    # ---- KPIs ----
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Actual Price", f"${row.actual_price:.2f}")
    c2.metric("Predicted Price", f"${row.predicted_price:.2f}")
    c3.metric("Absolute Error", f"${row.error:.2f}")
    c4.metric("Error %", f"{(row.error / row.actual_price) * 100:.2f}%")

    st.divider()

    # ---- ACTUAL vs PREDICTED ----
    st.subheader(f"📈 {asset} — Actual vs Predicted")

    fig = px.line(
        asset_forecast,
        x="date",
        y=["actual_price", "predicted_price"],
        markers=True,
        labels={"value": "Price ($)", "date": "Date"},
    )
    fig.update_layout(yaxis_tickprefix="$", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # ---- ERROR TREND ----
    st.subheader("📉 Error Over Time")

    err_fig = px.bar(
        asset_forecast,
        x="date",
        y="error",
        labels={"error": "Error ($)", "date": "Date"},
    )
    err_fig.update_layout(yaxis_tickprefix="$", height=300)
    st.plotly_chart(err_fig, use_container_width=True)

    # ---- PREDICTION TABLE (ADDED BACK) ----
    st.subheader("📋 Prediction History")

    table_df = asset_forecast.copy()
    table_df["Actual Price"] = table_df["actual_price"].map(lambda x: f"${x:.2f}")
    table_df["Predicted Price"] = table_df["predicted_price"].map(lambda x: f"${x:.2f}")
    table_df["Error"] = table_df["error"].map(lambda x: f"${x:.2f}")

    st.dataframe(
        table_df[["date", "Actual Price", "Predicted Price", "Error"]],
        use_container_width=True,
    )

# ==================================================
# MULTI ASSET MODE (RANGE WORKS CORRECTLY)
# ==================================================
else:
    selected_assets = st.sidebar.multiselect(
        "Select Assets",
        assets,
        default=assets[:2],
    )

    range_label = st.sidebar.selectbox(
        "History Range",
        list(RANGE_MAP.keys()),
        index=4,
    )

    days = RANGE_MAP[range_label]

    #  FILTER PER ASSET THEN RANGE
    multi_hist = history_df[history_df["asset"].isin(selected_assets)].copy()
    multi_hist = apply_history_range(multi_hist, days)

    st.subheader(f"📊 Price Trend — {range_label}")

    fig = px.line(
        multi_hist,
        x="date",
        y="price",
        color="asset",
        labels={"price": "Price ($)", "date": "Date"},
    )
    fig.update_layout(yaxis_tickprefix="$", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Latest Forecast Snapshot")

    latest = (
        forecast_df
        .sort_values("date")
        .groupby("asset")
        .tail(1)
    )

    st.dataframe(
        latest[["asset", "predicted_price", "actual_price", "error"]]
        .assign(
            predicted_price=lambda x: x.predicted_price.map(lambda v: f"${v:.2f}"),
            actual_price=lambda x: x.actual_price.map(lambda v: f"${v:.2f}"),
            error=lambda x: x.error.map(lambda v: f"${v:.2f}"),
        ),
        use_container_width=True,
    )
