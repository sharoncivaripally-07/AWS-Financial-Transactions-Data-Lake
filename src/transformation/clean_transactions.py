
import pandas as pd
import logging
from pathlib import Path

# 1. Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 2. Define input, output, and log locations
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "financial_transactions.csv"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"
LOG_FOLDER = PROJECT_ROOT / "logs"
LOG_FILE = LOG_FOLDER / "pipeline.log"

# 3. Configure pipeline logging
logger = logging.getLogger("financial_transactions_pipeline")


def configure_logging():
    """Configure logging to save messages in a file and display them."""
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        console_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)


def read_transactions(input_file=INPUT_FILE):
    """Read financial transactions from the CSV file."""
    print("Reading financial transactions...")

    df = pd.read_csv(input_file)

    print(f"Total records received: {len(df)}")
    logger.info("Total records received: %s", len(df))

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

    logger.info("Clean transactions saved successfully.")


def save_rejected_transactions(df, output_folder=OUTPUT_FOLDER):
    """Save rejected transactions as a CSV file."""
    output_folder.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        output_folder / "rejected_transactions.csv",
        index=False
    )

    logger.info("Rejected transactions saved successfully.")


def run_pipeline():
    """Run the complete financial transactions ETL pipeline."""
    configure_logging()

    logger.info("ETL pipeline started.")

    try:
        df = read_transactions()

        invalid = validate_transactions(df)
        duplicates = remove_duplicates(df)

        rejected_mask = invalid | duplicates

        rejected = df[rejected_mask].copy()
        cleaned = df[~rejected_mask].copy()

        print(f"Valid records: {len(cleaned)}")
        print(f"Rejected records: {len(rejected)}")

        logger.info("Valid records: %s", len(cleaned))
        logger.info("Rejected records: %s", len(rejected))

        save_clean_transactions(cleaned)
        save_rejected_transactions(rejected)

        print("ETL pipeline completed successfully!")
        logger.info("ETL pipeline completed successfully.")

    except Exception:
        logger.exception("ETL pipeline failed.")
        raise


if __name__ == "__main__":
    run_pipeline()

