import pandas as pd

def load_gold_silver_data():
    gold = pd.read_csv("data/raw/gold.csv")
    silver = pd.read_csv("data/raw/silver.csv")

    print("Gold data shape:", gold.shape)
    print("Silver data shape:", silver.shape)

    print("\nGold columns:")
    print(gold.columns)

    print("\nSilver columns:")
    print(silver.columns)

    return gold, silver


if __name__ == "__main__":
    gold_df, silver_df = load_gold_silver_data()
