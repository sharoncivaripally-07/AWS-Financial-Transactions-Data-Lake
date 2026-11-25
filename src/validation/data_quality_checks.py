from pathlib import Path
import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "clean_transactions.parquet"
)


def run_data_quality_checks(data_file=DATA_FILE):

    connection = duckdb.connect()

    connection.from_parquet(str(data_file)).create_view("transactions")

    checks = [
        (
            "Invalid currency",
            "currency IS NULL OR currency NOT IN ('USD')"
        ),
        (
            "Invalid transaction type",
            "transaction_type IS NULL OR transaction_type NOT IN "
            "('purchase', 'transfer', 'withdrawal')"
        ),
        (
            "Invalid payment method",
            "payment_method IS NULL OR payment_method NOT IN "
            "('bank_transfer', 'credit_card', 'debit_card', 'digital_wallet')"
        ),
        (
            "Invalid transaction status",
            "status IS NULL OR status NOT IN "
            "('pending', 'reversed', 'settled')"
        ),
        (
            "Invalid fraud flag",
            "fraud_flag IS NULL OR fraud_flag NOT IN (0, 1)"
        ),
        (
            "Missing merchant name",
            "merchant_name IS NULL OR TRIM(merchant_name) = ''"
        ),
        (
            "Invalid transaction amount",
            "amount IS NULL OR amount <= 0"
        ),
        (
            "Missing transaction timestamp",
            "transaction_timestamp IS NULL"
        ),
    ]

    print("\nFINANCIAL TRANSACTION DATA QUALITY REPORT")
    print("=" * 50)

    all_passed = True

    for check_name, condition in checks:

        query = f"""
            SELECT COUNT(*)
            FROM transactions
            WHERE {condition}
        """

        invalid_count = connection.execute(query).fetchone()[0]

        if invalid_count == 0:
            print(f"PASS: {check_name}")
        else:
            print(
                f"FAIL: {check_name} - "
                f"{invalid_count} invalid records"
            )
            all_passed = False

    duplicate_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT transaction_id
            FROM transactions
            GROUP BY transaction_id
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]

    if duplicate_count == 0:
        print("PASS: Duplicate transaction ID check")
    else:
        print(
            f"FAIL: Duplicate transaction ID check - "
            f"{duplicate_count} duplicate IDs"
        )
        all_passed = False

    print("=" * 50)

    if all_passed:
        print("ALL DATA QUALITY CHECKS PASSED!")
    else:
        print("DATA QUALITY ISSUES FOUND!")

    connection.close()

    return all_passed


if __name__ == "__main__":
    run_data_quality_checks()
