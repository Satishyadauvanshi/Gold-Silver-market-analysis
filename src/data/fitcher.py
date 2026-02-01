import yfinance as yf
from pathlib import Path

# Resolve project root
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_RAW = BASE_DIR / "data" / "raw"
DATA_RAW.mkdir(parents=True, exist_ok=True)

def fetch_gold_silver_data():
    print("Downloading Gold data...")
    gold = yf.download("GC=F", start="2015-01-01", progress=False)

    print("Downloading Silver data...")
    silver = yf.download("SI=F", start="2015-01-01", progress=False)

    gold_path = DATA_RAW / "gold.csv"
    silver_path = DATA_RAW / "silver.csv"

    gold.to_csv(gold_path)
    silver.to_csv(silver_path)

    print("Saved files:")
    print(gold_path)
    print(silver_path)

if __name__ == "__main__":
    fetch_gold_silver_data()

