
import pandas as pd

from src.transformation.clean_transactions import (
    validate_transactions,
    remove_duplicates,
)


def create_test_data():
    """Create sample transaction records for testing."""
    return pd.DataFrame({
        "transaction_id": ["T001", "T002", "T003"],
        "customer_id": ["C001", "C002", "C003"],
        "account_id": ["A001", "A002", "A003"],
        "amount": [100, 200, 300],
        "transaction_timestamp": [
            "2026-01-01",
            "2026-01-02",
            "2026-01-03"
        ]
    })


def test_missing_transaction_id_is_detected():
    df = create_test_data()
    df.loc[0, "transaction_id"] = None

    invalid = validate_transactions(df)

    assert invalid.tolist() == [True, False, False]


def test_invalid_amount_is_detected():
    df = create_test_data()
    df["amount"] = [100, 0, -50]

    invalid = validate_transactions(df)

    assert invalid.tolist() == [False, True, True]


def test_duplicate_transaction_id_is_detected():
    df = create_test_data()
    df.loc[2, "transaction_id"] = "T001"

    duplicates = remove_duplicates(df)

    assert duplicates.tolist() == [False, False, True]

