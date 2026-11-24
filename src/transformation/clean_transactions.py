
import pandas as pd
from pathlib import Path

# 1. Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 2. Define input and output locations
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "financial_transactions.csv"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# 3. EXTRACT: Read financial transactions
print("Reading financial transactions...")

df = pd.read_csv(INPUT_FILE)

print(f"Total records received: {len(df)}")

# 4. TRANSFORM: Clean and validate data

# Convert amount to numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Convert timestamp to datetime
df["transaction_timestamp"] = pd.to_datetime(
    df["transaction_timestamp"], errors="coerce"
)

# Identify invalid records
invalid = (
    df["transaction_id"].isna()
    | df["customer_id"].isna()
    | df["account_id"].isna()
    | df["amount"].isna()
    | (df["amount"] <= 0)
    | df["transaction_timestamp"].isna()
)

# Identify duplicate transaction IDs
duplicates = df["transaction_id"].duplicated(keep="first")

rejected = df[invalid | duplicates].copy()
cleaned = df[~(invalid | duplicates)].copy()

print(f"Valid records: {len(cleaned)}")
print(f"Rejected records: {len(rejected)}")

# 5. LOAD: Save clean data as Parquet
cleaned.to_parquet(
    OUTPUT_FOLDER / "clean_transactions.parquet",
    index=False
)

# Save rejected records for review
rejected.to_csv(
    OUTPUT_FOLDER / "rejected_transactions.csv",
    index=False
)

print("ETL pipeline completed successfully!")
