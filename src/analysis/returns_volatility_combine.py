import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def analyze_returns_and_volatility_combined():
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

    # Create combined plot with contrasting colors
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot with highly contrasting colors
    ax.plot(
        df["Date"],
        df["Gold_Return"],
        label=f"Gold Daily Returns (σ={gold_volatility:.4f})",
        color="#FF8C00",  # Dark orange
        linewidth=0.9,
        alpha=0.9
    )

    ax.plot(
        df["Date"],
        df["Silver_Return"],
        label=f"Silver Daily Returns (σ={silver_volatility:.4f})",
        color="#4169E1",  # Royal blue
        linewidth=0.9,
        alpha=0.7
    )

    # Add zero reference line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.4)

    # Styling
    ax.set_title("Daily Returns & Volatility: Gold vs Silver (Combined)", 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Daily Return", fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

    # Add insight box
    ax.text(
        0.98, 0.95,
        "Volatility Insight:\n" + 
        "• Larger spikes = higher volatility\n" +
        "• Silver (blue) shows wider swings\n" +
        "• Gold (orange) more stable",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=dict(boxstyle="round", facecolor='white', alpha=0.8, edgecolor='gray')
    )

    fig.tight_layout()

    output_path = BASE_DIR / "outputs" / "charts" / "daily_returns_gold_silver_combine.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')

    print("Combined returns chart saved to:", output_path)

    plt.show()
    plt.close(fig)

if __name__ == "__main__":
    analyze_returns_and_volatility_combined()