import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def analyze_returns_and_volatility():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate daily returns
    df["Gold_Return"] = df["Gold_Close"].pct_change()
    df["Silver_Return"] = df["Silver_Close"].pct_change()

    # Drop first row (NaN returns)
    df = df.dropna()

    # Calculate volatility (standard deviation)
    gold_volatility = df["Gold_Return"].std()
    silver_volatility = df["Silver_Return"].std()

    print("Gold Volatility (Daily):", round(gold_volatility, 4))
    print("Silver Volatility (Daily):", round(silver_volatility, 4))

    # Create separate subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    # Gold subplot
    ax1.plot(
        df["Date"],
        df["Gold_Return"],
        color="#B8860B",  # Dark goldenrod
        linewidth=0.7,
        alpha=0.8
    )
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    ax1.set_ylabel("Daily Return", fontsize=11)
    ax1.set_title("Gold Daily Returns (Lower Volatility)", fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.text(
        0.02, 0.95,
        f"Volatility (Std Dev): {gold_volatility:.4f}",
        transform=ax1.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.5)
    )

    # Silver subplot
    ax2.plot(
        df["Date"],
        df["Silver_Return"],
        color="#708090",  # Slate gray
        linewidth=0.7,
        alpha=0.8
    )
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    ax2.set_xlabel("Date", fontsize=11)
    ax2.set_ylabel("Daily Return", fontsize=11)
    ax2.set_title("Silver Daily Returns (Higher Volatility)", fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.text(
        0.02, 0.95,
        f"Volatility (Std Dev): {silver_volatility:.4f}",
        transform=ax2.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor='lightgray', alpha=0.5)
    )

    # Overall title
    fig.suptitle("Daily Returns & Volatility: Gold vs Silver", 
                 fontsize=14, fontweight='bold', y=0.995)

    fig.tight_layout()

    output_path = BASE_DIR / "outputs" / "charts" / "daily_returns_gold_silver.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')

    print("Returns chart saved to:", output_path)

    plt.show()
    plt.close(fig)

if __name__ == "__main__":
    analyze_returns_and_volatility()