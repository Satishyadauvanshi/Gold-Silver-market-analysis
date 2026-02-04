import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# Config
# -------------------------
st.set_page_config(
    page_title="Gold & Silver Market Dashboard",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Gold_Silver_Ratio"] = df["Gold_Close"] / df["Silver_Close"]
    return df

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.title("Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

df = df[(df["Date"] >= pd.to_datetime(date_range[0])) &
        (df["Date"] <= pd.to_datetime(date_range[1]))]

# -------------------------
# Header
# -------------------------
st.title("📊 Gold & Silver Market Analysis")
st.caption("Interactive dashboard for Product / BI / Analytics roles")

# -------------------------
# KPI Row
# -------------------------
col1, col2, col3 = st.columns(3)

gold_return = (df["Gold_Close"].iloc[-1] / df["Gold_Close"].iloc[0] - 1) * 100
silver_return = (df["Silver_Close"].iloc[-1] / df["Silver_Close"].iloc[0] - 1) * 100
avg_ratio = df["Gold_Silver_Ratio"].mean()

col1.metric("Gold Total Return", f"{gold_return:.2f}%")
col2.metric("Silver Total Return", f"{silver_return:.2f}%")
col3.metric("Avg Gold–Silver Ratio", f"{avg_ratio:.1f}")

st.markdown("---")

# -------------------------
# Price Trends
# -------------------------
st.subheader("Gold vs Silver Price Trends")

fig_price = px.line(
    df,
    x="Date",
    y=["Gold_Close", "Silver_Close"],
    labels={"value": "Price", "variable": "Asset"},
)
st.plotly_chart(fig_price, width="stretch")

# -------------------------
# Normalized Performance
# -------------------------
st.subheader("Normalized Performance (Base = 100)")

df_norm = df.copy()
df_norm["Gold (Normalized)"] = df_norm["Gold_Close"] / df_norm["Gold_Close"].iloc[0] * 100
df_norm["Silver (Normalized)"] = df_norm["Silver_Close"] / df_norm["Silver_Close"].iloc[0] * 100

fig_norm = px.line(
    df_norm,
    x="Date",
    y=["Gold (Normalized)", "Silver (Normalized)"],
    labels={"value": "Normalized Value", "variable": "Asset"},
)
st.plotly_chart(fig_norm, width="stretch")

# -------------------------
# Gold–Silver Ratio
# -------------------------
st.subheader("Gold–Silver Ratio")

fig_ratio = px.line(
    df,
    x="Date",
    y="Gold_Silver_Ratio",
    labels={"Gold_Silver_Ratio": "Gold / Silver Ratio"},
)
st.plotly_chart(fig_ratio, width="stretch")

st.markdown(
    "💡 **Insight:** Higher ratio → Silver undervalued relative to Gold. "
    "Lower ratio → Silver outperforming Gold."
)

# -------------------------
# Volatility (Rolling)
# -------------------------
st.subheader("Rolling Volatility (30-Day)")

df["Gold_Return"] = df["Gold_Close"].pct_change()
df["Silver_Return"] = df["Silver_Close"].pct_change()

df["Gold_Vol_30"] = df["Gold_Return"].rolling(30).std()
df["Silver_Vol_30"] = df["Silver_Return"].rolling(30).std()

fig_vol = px.line(
    df,
    x="Date",
    y=["Gold_Vol_30", "Silver_Vol_30"],
    labels={"value": "Volatility", "variable": "Asset"},
)
st.plotly_chart(fig_vol, width="stretch")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption(
    "This dashboard focuses on insight communication and decision support, "
    "not trading recommendations."
)
