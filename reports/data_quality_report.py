
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CLEAN_FILE = PROJECT_ROOT / "data" / "processed" / "clean_transactions.parquet"
REJECTED_FILE = PROJECT_ROOT / "data" / "processed" / "rejected_transactions.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "data_quality_report.txt"


def generate_report():

    clean_df = pd.read_parquet(CLEAN_FILE)
    rejected_df = pd.read_csv(REJECTED_FILE)

    valid_count = len(clean_df)
    rejected_count = len(rejected_df)
    total_count = valid_count + rejected_count

    quality_rate = (valid_count / total_count) * 100
    rejection_rate = (rejected_count / total_count) * 100

    invalid_amounts = pd.to_numeric(
        rejected_df["amount"], errors="coerce"
    ).le(0).sum()

    missing_transaction_id = rejected_df["transaction_id"].isna().sum()
    missing_customer_id = rejected_df["customer_id"].isna().sum()
    missing_account_id = rejected_df["account_id"].isna().sum()
    missing_timestamp = rejected_df["transaction_timestamp"].isna().sum()

    report = f"""
FINANCIAL TRANSACTIONS DATA QUALITY REPORT
============================================

OVERALL SUMMARY

Total Transactions: {total_count}
Valid Transactions: {valid_count}
Rejected Transactions: {rejected_count}

Data Quality Rate: {quality_rate:.2f}%
Rejection Rate: {rejection_rate:.2f}%

REJECTION REASON ANALYSIS

Invalid or Non-Positive Amounts: {invalid_amounts}
Missing Transaction IDs: {missing_transaction_id}
Missing Customer IDs: {missing_customer_id}
Missing Account IDs: {missing_account_id}
Missing Timestamps: {missing_timestamp}

============================================
REPORT GENERATED SUCCESSFULLY
"""

    print(report)

    REPORT_FILE.write_text(report)

    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
