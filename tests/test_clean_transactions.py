
import pandas as pd


def test_missing_transaction_id_is_detected():
    df = pd.DataFrame({
        "transaction_id": [None, "T002"],
        "customer_id": ["C001", "C002"],
        "account_id": ["A001", "A002"],
        "amount": [100, 200],
        "transaction_timestamp": ["2026-01-01", "2026-01-02"]
    })

    invalid = (
        df["transaction_id"].isna()
        | df["customer_id"].isna()
        | df["account_id"].isna()
        | df["amount"].isna()
        | (df["amount"] <= 0)
        | pd.to_datetime(
            df["transaction_timestamp"], errors="coerce"
        ).isna()
    )

    assert invalid.iloc[0] == True
    assert invalid.iloc[1] == False


def test_invalid_amount_is_detected():
    df = pd.DataFrame({
        "amount": [100, 0, -50]
    })

    invalid = df["amount"].isna() | (df["amount"] <= 0)

    assert invalid.tolist() == [False, True, True]


def test_duplicate_transaction_id_is_detected():
    df = pd.DataFrame({
        "transaction_id": ["T001", "T002", "T001"]
    })

    duplicates = df["transaction_id"].duplicated(keep="first")

    assert duplicates.tolist() == [False, False, True]
