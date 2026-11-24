# Initial data quality rules

1. `transaction_id` must not be null and must be unique.
2. `customer_id` and `account_id` must not be null.
3. `transaction_timestamp` must parse as a timestamp.
4. `amount` must be numeric; refunds may be negative.
5. `currency` must be a supported three-letter code (the sample uses USD).
6. `transaction_type` must be one of purchase, refund, withdrawal, transfer.
7. `status` must be one of settled, pending, reversed.
8. `fraud_flag` must be 0 or 1.
9. Invalid records should be written to a quarantine/rejects prefix with a reason, not silently discarded.
