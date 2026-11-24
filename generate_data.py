"""Generate synthetic financial transaction data for the AWS Financial Data Lake project.

All records are fictional. Do not use real customer or payment-card information.
Run: python src/ingestion/generate_data.py
"""
from pathlib import Path
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

def generate_transactions(n=1000):
    categories = ["grocery", "restaurants", "travel", "electronics", "fuel", "healthcare", "retail", "utilities"]
    merchants = ["Fresh Market", "Harbor Cafe", "Skyway Airlines", "TechHub", "QuickFuel",
                 "Community Pharmacy", "Everyday Goods", "Power & Light"]
    cities = [("New York", "US"), ("Chicago", "US"), ("Dallas", "US"), ("Seattle", "US"), ("Atlanta", "US")]
    types = ["purchase", "refund", "withdrawal", "transfer"]
    methods = ["debit_card", "credit_card", "bank_transfer", "digital_wallet"]
    statuses = ["settled", "settled", "settled", "pending", "reversed"]
    start = datetime(2025, 1, 1)
    rows = []
    for i in range(n):
        amount = round(float(np.random.lognormal(3.3, 1.0)), 2)
        tx_type = random.choices(types, weights=[78, 5, 7, 10])[0]
        if tx_type == "refund":
            amount = -amount
        city, country = random.choice(cities)
        rows.append({
            "transaction_id": f"TXN{i+1:07d}",
            "customer_id": f"CUST{random.randint(1, 250):05d}",
            "account_id": f"ACC{random.randint(1, 350):05d}",
            "transaction_timestamp": (start + timedelta(minutes=random.randint(0, 365*24*60))).isoformat(timespec="seconds"),
            "amount": amount,
            "currency": "USD",
            "transaction_type": tx_type,
            "merchant_category": random.choice(categories),
            "merchant_name": random.choice(merchants),
            "city": city,
            "country": country,
            "payment_method": random.choice(methods),
            "status": random.choice(statuses),
            "fraud_flag": int(random.random() < 0.015)
        })
    return pd.DataFrame(rows).sort_values("transaction_timestamp")

if __name__ == "__main__":
    output = Path(__file__).resolve().parents[2] / "data" / "raw" / "financial_transactions.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_transactions().to_csv(output, index=False)
    print(f"Wrote synthetic transactions to {output}")
