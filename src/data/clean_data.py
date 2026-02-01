import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"
DATA_PROCESSED.mkdir(exist_ok=True)

def load_yfinance_csv(path):
    """
    Robust loader for yfinance CSVs.
    Handles:
    - Metadata rows (Ticker, etc.)
    - Date stored in first column
    """
    df = pd.read_csv(path)

    # Rename first column to Date
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "Date"})

    # Convert Date column safely
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows where Date is invalid (Ticker, NaN, etc.)
    df = df.dropna(subset=["Date"])

    return df

def clean_gold_silver_data():
    # Load raw data
    gold = load_yfinance_csv(DATA_RAW / "gold.csv")
    silver = load_yfinance_csv(DATA_RAW / "silver.csv")

    # Rename Close columns
    gold = gold.rename(columns={"Close": "Gold_Close"})
    silver = silver.rename(columns={"Close": "Silver_Close"})

    # Select required columns
    gold = gold[["Date", "Gold_Close"]]
    silver = silver[["Date", "Silver_Close"]]

    # Merge datasets (SQL INNER JOIN)
    merged = pd.merge(gold, silver, on="Date", how="inner")

    # Sort by date
    merged = merged.sort_values("Date")

    # Save cleaned data
    output_path = DATA_PROCESSED / "gold_silver_cleaned.csv"
    merged.to_csv(output_path, index=False)

    print("✅ Cleaned data saved to:")
    print(output_path)
    print("Final dataset shape:", merged.shape)
    print("\nSample rows:")
    print(merged.head())

if __name__ == "__main__":
    clean_gold_silver_data()
