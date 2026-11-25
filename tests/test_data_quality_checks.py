
import pandas as pd
import pytest

from src.validation.data_quality_checks import run_data_quality_checks


def test_data_quality_checks_pass():
    result = run_data_quality_checks()

    assert result is True


@pytest.mark.parametrize(
    "column, invalid_value",
    [
        ("currency", "EUR"),
        ("payment_method", "crypto"),
        ("merchant_name", None),
        ("fraud_flag", 2),
    ],
)
def test_invalid_data_is_detected(tmp_path, column, invalid_value):

    sample_data = {
        "transaction_id": ["TXN001"],
        "currency": ["USD"],
        "transaction_type": ["purchase"],
        "payment_method": ["credit_card"],
        "status": ["settled"],
        "fraud_flag": [0],
        "merchant_name": ["Amazon"],
        "amount": [100.00],
        "transaction_timestamp": ["2026-01-15 10:00:00"],
    }

    df = pd.DataFrame(sample_data)

    df[column] = invalid_value

    test_file = tmp_path / "test_transactions.parquet"
    df.to_parquet(test_file, index=False)

    result = run_data_quality_checks(data_file=test_file)

    assert result is False
