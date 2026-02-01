import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

def plot_gold_silver_trends():
    df = pd.read_csv(DATA_PROCESSED / "gold_silver_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(df["Date"], df["Gold_Close"], label="Gold Price")
    ax.plot(df["Date"], df["Silver_Close"], label="Silver Price")

    ax.set_title("Gold vs Silver Price Trends")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

    fig.tight_layout()

    output_path = BASE_DIR / "outputs" / "charts" / "gold_vs_silver_trend.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path)

    print("Chart saved to:", output_path)

    plt.show()
    plt.close(fig)


if __name__ == "__main__":
    plot_gold_silver_trends()
