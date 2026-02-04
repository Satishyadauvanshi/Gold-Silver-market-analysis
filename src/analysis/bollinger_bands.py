import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def plot_bollinger_bands(asset="Gold"):
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    
    if asset == "Gold":
        price_col = "Gold_Close"
        color = "#B8860B"  # Gold tone
        fill_color = "#FFD700"  # Lighter gold for fill
    else:
        price_col = "Silver_Close"
        color = "#708090"  # Silver tone
        fill_color = "#C0C0C0"  # Lighter silver for fill
    
    # Bollinger Band parameters
    window = 20
    df["MA"] = df[price_col].rolling(window).mean()
    df["STD"] = df[price_col].rolling(window).std()
    df["Upper_Band"] = df["MA"] + 2 * df["STD"]
    df["Lower_Band"] = df["MA"] - 2 * df["STD"]
    
    # Calculate %B (Position within bands) - KEY METRIC
    df["Percent_B"] = (df[price_col] - df["Lower_Band"]) / (df["Upper_Band"] - df["Lower_Band"])
    
    # Identify buy/sell signals (when price touches bands)
    df["Buy_Signal"] = (df[price_col] <= df["Lower_Band"]) & (df[price_col].shift(1) > df["Lower_Band"].shift(1))
    df["Sell_Signal"] = (df[price_col] >= df["Upper_Band"]) & (df[price_col].shift(1) < df["Upper_Band"].shift(1))
    
    # Calculate statistics
    total_buy_signals = df["Buy_Signal"].sum()
    total_sell_signals = df["Sell_Signal"].sum()
    current_price = df[price_col].iloc[-1]
    current_ma = df["MA"].iloc[-1]
    current_upper = df["Upper_Band"].iloc[-1]
    current_lower = df["Lower_Band"].iloc[-1]
    current_percent_b = df["Percent_B"].iloc[-1]
    
    # Determine current position
    if current_percent_b > 1:
        position = "OVERBOUGHT"
        signal_color = "#E74C3C"
    elif current_percent_b < 0:
        position = "OVERSOLD"
        signal_color = "#27AE60"
    else:
        position = "NEUTRAL"
        signal_color = "#95A5A6"
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), 
                                     gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    
    # ===== MAIN CHART =====
    # Plot price and bands
    ax1.plot(df["Date"], df[price_col], label=f"{asset} Price", 
             color=color, linewidth=1.5, alpha=0.9, zorder=3)
    ax1.plot(df["Date"], df["MA"], label="20-Day MA (Middle Band)", 
             color="black", linewidth=1.5, linestyle="--", zorder=2)
    
    # Plot upper and lower bands
    ax1.plot(df["Date"], df["Upper_Band"], color=color, 
             linewidth=1, alpha=0.5, linestyle=":", zorder=1)
    ax1.plot(df["Date"], df["Lower_Band"], color=color, 
             linewidth=1, alpha=0.5, linestyle=":", zorder=1)
    
    # Fill between bands
    ax1.fill_between(
        df["Date"],
        df["Upper_Band"],
        df["Lower_Band"],
        color=fill_color,
        alpha=0.15,
        label="±2σ Bands (95% confidence)"
    )
    
    # Mark buy/sell signals
    buy_dates = df[df["Buy_Signal"]]["Date"]
    buy_prices = df[df["Buy_Signal"]][price_col]
    sell_dates = df[df["Sell_Signal"]]["Date"]
    sell_prices = df[df["Sell_Signal"]][price_col]
    
    ax1.scatter(buy_dates, buy_prices, color="#27AE60", marker="^", 
                s=100, label=f"Buy Signal ({total_buy_signals})", zorder=5, edgecolors='black', linewidth=0.5)
    ax1.scatter(sell_dates, sell_prices, color="#E74C3C", marker="v", 
                s=100, label=f"Sell Signal ({total_sell_signals})", zorder=5, edgecolors='black', linewidth=0.5)
    
    # Styling
    ax1.set_title(f"{asset} Price with Bollinger Bands (20-Day, 2σ)", 
                  fontsize=15, fontweight="bold", pad=15)
    ax1.set_ylabel("Price (USD)", fontsize=12, fontweight="bold")
    ax1.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle="--")
    
    # Add insight box
    insight_text = (
        f"Current Status: {position}\n"
        f"Price: ${current_price:.2f}\n"
        f"Upper Band: ${current_upper:.2f}\n"
        f"MA (Middle): ${current_ma:.2f}\n"
        f"Lower Band: ${current_lower:.2f}\n"
        f"%B: {current_percent_b:.2f}"
    )
    
    ax1.text(0.02, 0.97, insight_text,
             transform=ax1.transAxes, fontsize=9,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor=signal_color, alpha=0.3, edgecolor=signal_color, linewidth=2))
    
    # ===== %B INDICATOR (BOTTOM CHART) =====
    ax2.plot(df["Date"], df["Percent_B"], color=color, linewidth=1.2, alpha=0.8)
    ax2.axhline(y=1, color='#E74C3C', linestyle='--', linewidth=1, alpha=0.7, label="Overbought (>1)")
    ax2.axhline(y=0, color='#27AE60', linestyle='--', linewidth=1, alpha=0.7, label="Oversold (<0)")
    ax2.axhline(y=0.5, color='black', linestyle=':', linewidth=1, alpha=0.5, label="Middle (0.5)")
    
    # Shade overbought/oversold zones
    ax2.fill_between(df["Date"], 1, 1.5, color='#E74C3C', alpha=0.1)
    ax2.fill_between(df["Date"], 0, -0.5, color='#27AE60', alpha=0.1)
    
    ax2.set_ylabel("%B Indicator", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax2.set_ylim(-0.5, 1.5)
    ax2.legend(loc='upper left', fontsize=9, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle="--")
    
    fig.tight_layout()
    
    # Save
    output_path = BASE_DIR / "outputs" / "charts" / f"{asset.lower()}_bollinger_bands.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    
    # Print statistics
    print(f"\n{'='*50}")
    print(f"{asset} Bollinger Bands Analysis")
    print(f"{'='*50}")
    print(f"Total Buy Signals (touched lower band): {total_buy_signals}")
    print(f"Total Sell Signals (touched upper band): {total_sell_signals}")
    print(f"Current Price: ${current_price:.2f}")
    print(f"Current %B: {current_percent_b:.2f} ({position})")
    print(f"Band Width: ${current_upper - current_lower:.2f}")
    print(f"\nChart saved to: {output_path}")
    print(f"{'='*50}\n")
    
    plt.show()
    plt.close(fig)

if __name__ == "__main__":
    plot_bollinger_bands("Gold")
    plot_bollinger_bands("Silver")