import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# -----------------------------
# Utility: Max Drawdown
# -----------------------------
def calculate_max_drawdown(equity):
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    return drawdown.min() * 100


# -----------------------------
# Backtest Function
# -----------------------------
def backtest_bollinger_strategy(
    asset="Gold",
    initial_capital=100_000,
    transaction_cost=0.001  # 0.1% per trade
):
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    price_col = "Gold_Close" if asset == "Gold" else "Silver_Close"

    # Bollinger Bands
    window = 20
    df["MA"] = df[price_col].rolling(window).mean()
    df["STD"] = df[price_col].rolling(window).std()
    df["Upper"] = df["MA"] + 2 * df["STD"]
    df["Lower"] = df["MA"] - 2 * df["STD"]

    df = df.dropna().reset_index(drop=True)

    # Signals (NO look-ahead bias)
    df["Buy"] = (df[price_col] <= df["Lower"]) & (df[price_col].shift(1) > df["Lower"].shift(1))
    df["Sell"] = (df[price_col] >= df["Upper"]) & (df[price_col].shift(1) < df["Upper"].shift(1))

    cash = initial_capital
    position = 0.0
    equity_curve = []

    trades = []

    for i in range(len(df)):
        price = df.loc[i, price_col]
        date = df.loc[i, "Date"]

        # BUY
        if df.loc[i, "Buy"] and position == 0:
            position = (cash * (1 - transaction_cost)) / price
            entry_price = price
            cash = 0

            trades.append({"Date": date, "Type": "BUY", "Price": price})

        # SELL
        elif df.loc[i, "Sell"] and position > 0:
            cash = position * price * (1 - transaction_cost)
            pnl_pct = (price - entry_price) / entry_price * 100
            position = 0

            trades.append({
                "Date": date,
                "Type": "SELL",
                "Price": price,
                "PnL_%": pnl_pct
            })

        total_equity = cash if position == 0 else position * price
        equity_curve.append(total_equity)

    df["Equity"] = equity_curve

    # -----------------------------
    # Performance Metrics
    # -----------------------------
    final_equity = df["Equity"].iloc[-1]
    total_return = (final_equity / initial_capital - 1) * 100
    max_dd = calculate_max_drawdown(df["Equity"])

    buy_hold_return = (
        df[price_col].iloc[-1] / df[price_col].iloc[0] - 1
    ) * 100

    trades_df = pd.DataFrame(trades)
    sell_trades = trades_df[trades_df["Type"] == "SELL"]

    win_rate = (sell_trades["PnL_%"] > 0).mean() * 100 if not sell_trades.empty else 0
    avg_trade = sell_trades["PnL_%"].mean() if not sell_trades.empty else 0

    # -----------------------------
    # Print Summary
    # -----------------------------
    print("\n" + "=" * 60)
    print(f"{asset} – Bollinger Band Backtest (Final)")
    print("=" * 60)
    print(f"Initial Capital:        ${initial_capital:,.0f}")
    print(f"Final Capital:          ${final_equity:,.0f}")
    print(f"Strategy Return:        {total_return:.2f}%")
    print(f"Buy & Hold Return:      {buy_hold_return:.2f}%")
    print(f"Max Drawdown:           {max_dd:.2f}%")
    print(f"Total Trades:           {len(sell_trades)}")
    print(f"Win Rate:               {win_rate:.2f}%")
    print(f"Average Trade PnL:      {avg_trade:.2f}%")
    print("Transaction Cost:       0.1% per trade")
    print("Note: Results are illustrative, not financial advice.")
    print("=" * 60)

    # -----------------------------
    # Equity Curve Plot
    # -----------------------------
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df["Date"], df["Equity"], label="Strategy Equity", color="purple")

    ax.set_title(f"{asset} Bollinger Strategy – Equity Curve")
    ax.set_xlabel("Date")
    ax.set_ylabel("Portfolio Value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    output_path = BASE_DIR / "outputs" / "charts" / f"{asset.lower()}_equity_curve.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.show()
    plt.close(fig)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    backtest_bollinger_strategy("Gold")
    backtest_bollinger_strategy("Silver")
