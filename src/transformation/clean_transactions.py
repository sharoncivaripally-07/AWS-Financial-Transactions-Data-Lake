
import pandas as pd
from pathlib import Path

# 1. Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 2. Define input and output locations
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "financial_transactions.csv"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"


def read_transactions(input_file=INPUT_FILE):
    """Read financial transactions from the CSV file."""
    print("Reading financial transactions...")

    df = pd.read_csv(input_file)

    print(f"Total records received: {len(df)}")

    return df


def validate_transactions(df):
    """Identify records with missing or invalid values."""
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_timestamp"], errors="coerce"
    )

    invalid = (
        df["transaction_id"].isna()
        | df["customer_id"].isna()
        | df["account_id"].isna()
        | df["amount"].isna()
        | (df["amount"] <= 0)
        | df["transaction_timestamp"].isna()
    )

    return invalid


def remove_duplicates(df):
    """Identify duplicate transaction IDs."""
    duplicates = df["transaction_id"].duplicated(keep="first")

    return duplicates


def save_clean_transactions(df, output_folder=OUTPUT_FOLDER):
    """Save valid transactions as a Parquet file."""
    output_folder.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        output_folder / "clean_transactions.parquet",
        index=False
    )


def save_rejected_transactions(df, output_folder=OUTPUT_FOLDER):
    """Save rejected transactions as a CSV file."""
    output_folder.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_folder / "rejected_transactions.csv",
        index=False
    )


def run_pipeline():
    """Run the complete financial transactions ETL pipeline."""
    df = read_transactions()

    invalid = validate_transactions(df)
    duplicates = remove_duplicates(df)

    rejected_mask = invalid | duplicates

    rejected = df[rejected_mask].copy()
    cleaned = df[~rejected_mask].copy()

    print(f"Valid records: {len(cleaned)}")
    print(f"Rejected records: {len(rejected)}")

    save_clean_transactions(cleaned)
    save_rejected_transactions(rejected)

    print("ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()

