import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Gold & Silver Market Dashboard",
    layout="wide"
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Gold_Silver_Ratio"] = df["Gold_Close"] / df["Silver_Close"]
    return df

df = load_data()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.title("Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Safe handling (prevents crash)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("📊 Gold & Silver Market Analysis")
st.caption("Interactive BI-style dashboard for Product & Analytics roles")

# --------------------------------------------------
# TABS (NO SCROLLING DESIGN)
# --------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Volatility", "Gold–Silver Ratio", "Strategy View"]
)

# ==================================================
# TAB 1 — OVERVIEW
# ==================================================
with tab1:
    st.subheader("Market Overview")

    col1, col2, col3 = st.columns(3)

    gold_return = (df["Gold_Close"].iloc[-1] / df["Gold_Close"].iloc[0] - 1) * 100
    silver_return = (df["Silver_Close"].iloc[-1] / df["Silver_Close"].iloc[0] - 1) * 100
    avg_ratio = df["Gold_Silver_Ratio"].mean()

    col1.metric("Gold Total Return", f"{gold_return:.2f}%")
    col2.metric("Silver Total Return", f"{silver_return:.2f}%")
    col3.metric("Avg Gold–Silver Ratio", f"{avg_ratio:.1f}")

    fig_price = px.line(
        df,
        x="Date",
        y=["Gold_Close", "Silver_Close"],
        labels={"value": "Price", "variable": "Asset"},
        title="Gold vs Silver Price Trends"
    )

    st.plotly_chart(fig_price, width="stretch", key="price_trends")

# ==================================================
# TAB 2 — VOLATILITY
# ==================================================
with tab2:
    st.subheader("Volatility Comparison (30-Day Rolling)")

    df["Gold_Return"] = df["Gold_Close"].pct_change()
    df["Silver_Return"] = df["Silver_Close"].pct_change()

    df["Gold_Vol_30"] = df["Gold_Return"].rolling(30).std()
    df["Silver_Vol_30"] = df["Silver_Return"].rolling(30).std()

    fig_vol = px.line(
        df,
        x="Date",
        y=["Gold_Vol_30", "Silver_Vol_30"],
        labels={"value": "Volatility", "variable": "Asset"},
        title="Rolling Volatility Comparison"
    )

    st.plotly_chart(fig_vol, width="stretch", key="volatility_chart")

    st.caption("Silver consistently exhibits higher volatility than Gold.")

# ==================================================
# TAB 3 — GOLD–SILVER RATIO
# ==================================================
with tab3:
    st.subheader("Gold–Silver Ratio")

    fig_ratio = px.line(
        df,
        x="Date",
        y="Gold_Silver_Ratio",
        labels={"Gold_Silver_Ratio": "Gold / Silver Ratio"},
        title="Gold–Silver Ratio Over Time"
    )

    st.plotly_chart(fig_ratio, width="stretch", key="ratio_chart")

    st.caption(
        "Higher ratio → Silver undervalued relative to Gold. "
        "Lower ratio → Silver outperforming Gold."
    )

# ==================================================
# TAB 4 — STRATEGY VIEW
# ==================================================
with tab4:
    st.subheader("Normalized Performance (Buy & Hold Perspective)")

    df_norm = df.copy()
    df_norm["Gold (Normalized)"] = df_norm["Gold_Close"] / df_norm["Gold_Close"].iloc[0] * 100
    df_norm["Silver (Normalized)"] = df_norm["Silver_Close"] / df_norm["Silver_Close"].iloc[0] * 100

    fig_norm = px.line(
        df_norm,
        x="Date",
        y=["Gold (Normalized)", "Silver (Normalized)"],
        labels={"value": "Index Value (Base = 100)", "variable": "Asset"},
        title="Normalized Performance Comparison"
    )

    st.plotly_chart(fig_norm, width="stretch", key="normalized_chart")

    st.markdown(
        "**Insight:** Trend-following buy-and-hold strategies captured long-term gains "
        "more effectively than short-term mean-reversion signals."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")
st.caption("Built as a portfolio-ready BI dashboard • Educational & analytical use only")
