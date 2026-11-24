# AWS Financial Transactions Data Lake

An end-to-end portfolio project that demonstrates a governed financial transaction data lake using AWS.

> **Data safety:** The included dataset is entirely synthetic. It contains no real customer, bank-account, or payment-card information. Do not upload real financial or personally identifiable information to this public repository.

## Business scenario
A fictional financial services company needs to ingest transaction records, validate and transform them, store analytics-ready data efficiently, and support SQL-based reporting.

## Target architecture
1. **Raw zone (Amazon S3):** land source CSV files without changing the original records.
2. **Catalog (AWS Glue Data Catalog):** maintain table and schema metadata.
3. **ETL (AWS Glue + PySpark):** validate records, standardize types, remove duplicates, and derive reporting fields.
4. **Curated zone (Amazon S3 + Parquet):** store cleaned data, partitioned by transaction date.
5. **Analytics (Amazon Athena):** query curated transaction data.
6. **Warehouse (Amazon Redshift):** load dimensional and fact tables for BI workloads.
7. **Orchestration (AWS Step Functions + Lambda):** coordinate and trigger pipeline stages.
8. **Observability (Amazon CloudWatch):** capture logs, metrics, and failures.

## Repository structure
```text
aws-financial-data-lake/
├── data/
│   └── raw/
│       └── financial_transactions.csv
├── src/
│   ├── ingestion/
│   │   └── generate_data.py
│   └── transformation/
├── sql/
│   └── athena/
├── infrastructure/
├── docs/
└── README.md
```

## Dataset fields
`transaction_id`, `customer_id`, `account_id`, `transaction_timestamp`, `amount`, `currency`, `transaction_type`, `merchant_category`, `merchant_name`, `city`, `country`, `payment_method`, `status`, `fraud_flag`.

## Local setup
```bash
python -m pip install pandas numpy
python src/ingestion/generate_data.py
```

The included sample file contains 1,000 synthetic transactions. The generator can recreate it.

## Planned milestones
- [ ] Milestone 1: inspect the sample data and define data quality rules.
- [ ] Milestone 2: create an S3 bucket and upload the raw CSV to a raw zone.
- [ ] Milestone 3: create a Glue database, crawler, and Data Catalog table.
- [ ] Milestone 4: write a PySpark Glue ETL job to validate, deduplicate, and convert CSV to partitioned Parquet.
- [ ] Milestone 5: query curated data with Athena.
- [ ] Milestone 6: model transaction facts and dimensions and load Redshift.
- [ ] Milestone 7: orchestrate the workflow and add monitoring.
- [ ] Milestone 8: document architecture, tests, sample queries, and screenshots.

## Important design notes
- Keep raw data immutable; write transformed output to a separate curated prefix.
- Use least-privilege IAM roles and encryption for S3 data.
- Partition curated data by transaction year/month/day where appropriate.
- Never commit AWS access keys, secrets, `.env` files, or real customer data.
- AWS resources can incur charges. Create only the resources needed for each milestone and delete them when finished.
