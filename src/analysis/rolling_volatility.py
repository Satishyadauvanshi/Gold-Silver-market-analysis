import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def analyze_rolling_volatility_improved():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate daily returns
    df["Gold_Return"] = df["Gold_Close"].pct_change()
    df["Silver_Return"] = df["Silver_Close"].pct_change()

    # Calculate rolling volatility
    df["Gold_Vol_30"] = df["Gold_Return"].rolling(window=30).std()
    df["Gold_Vol_90"] = df["Gold_Return"].rolling(window=90).std()
    df["Silver_Vol_30"] = df["Silver_Return"].rolling(window=30).std()
    df["Silver_Vol_90"] = df["Silver_Return"].rolling(window=90).std()

    # Create improved subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)

    # Gold subplot - Better colors
    ax1.plot(df["Date"], df["Gold_Vol_30"], 
             label="30-Day Volatility", color="#FF6B35", linewidth=1.2, alpha=0.8)
    ax1.plot(df["Date"], df["Gold_Vol_90"], 
             label="90-Day Volatility", color="#004E89", linewidth=1.5, alpha=0.9)
    
    ax1.set_ylabel("Volatility (Std Dev)", fontsize=12, fontweight='bold')
    ax1.set_title("Gold Rolling Volatility", fontsize=13, fontweight='bold', pad=10)
    ax1.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax1.grid(True, alpha=0.3, linestyle='--')
    
    # Add interpretation box
    ax1.text(0.98, 0.97, 
             "30-Day: Quick reactions to market changes\n90-Day: Smoothed long-term trend",
             transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    # Silver subplot - Same color scheme
    ax2.plot(df["Date"], df["Silver_Vol_30"], 
             label="30-Day Volatility", color="#FF6B35", linewidth=1.2, alpha=0.8)
    ax2.plot(df["Date"], df["Silver_Vol_90"], 
             label="90-Day Volatility", color="#004E89", linewidth=1.5, alpha=0.9)
    
    ax2.set_xlabel("Date", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Volatility (Std Dev)", fontsize=12, fontweight='bold')
    ax2.set_title("Silver Rolling Volatility", fontsize=13, fontweight='bold', pad=10)
    ax2.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax2.grid(True, alpha=0.3, linestyle='--')
    
    # Add key insight
    ax2.text(0.98, 0.97,
             "Silver shows 2-3x higher volatility than Gold\nNotice the dramatic spikes during crisis periods",
             transform=ax2.transAxes, fontsize=9,
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Overall title
    fig.suptitle("Rolling Volatility Comparison (30-Day vs 90-Day)", 
                 fontsize=15, fontweight='bold', y=0.995)

    fig.tight_layout()

    output_path = BASE_DIR / "outputs" / "charts" / "rolling_volatility_comparison.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')

    print(f"Rolling volatility chart saved to: {output_path}")
    
    # Print summary statistics
    print("\n=== Volatility Summary ===")
    print(f"Gold 30-Day Average: {df['Gold_Vol_30'].mean():.4f}")
    print(f"Gold 90-Day Average: {df['Gold_Vol_90'].mean():.4f}")
    print(f"Silver 30-Day Average: {df['Silver_Vol_30'].mean():.4f}")
    print(f"Silver 90-Day Average: {df['Silver_Vol_90'].mean():.4f}")
    print(f"\nSilver/Gold Volatility Ratio: {df['Silver_Vol_30'].mean() / df['Gold_Vol_30'].mean():.2f}x")

    plt.show()
    plt.close(fig)

if __name__ == "__main__":
    analyze_rolling_volatility_improved()