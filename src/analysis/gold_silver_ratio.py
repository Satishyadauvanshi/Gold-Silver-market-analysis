import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def plot_gold_silver_ratio():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate ratio
    df["Gold_Silver_Ratio"] = df["Gold_Close"] / df["Silver_Close"]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["Date"], df["Gold_Silver_Ratio"], color="purple")

    ax.set_title("Gold–Silver Ratio Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Gold / Silver Ratio")

    ax.text(
    0.02, 0.95,
    "Gold–Silver Ratio = Gold Price ÷ Silver Price",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round", alpha=0.2)
    )

    fig.tight_layout()

    output_path = BASE_DIR / "outputs" / "charts" / "gold_silver_ratio.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)

    print("Gold–Silver ratio chart saved to:", output_path)

    plt.show()
    plt.close(fig)

if __name__ == "__main__":
    plot_gold_silver_ratio()
