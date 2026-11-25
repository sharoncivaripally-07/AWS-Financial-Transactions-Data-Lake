-- AWS Financial Transactions Data Lake
-- Star Schema Data Warehouse

-- 1. Customer Dimension
CREATE OR REPLACE TABLE dim_customer AS
SELECT DISTINCT
    customer_id
FROM read_parquet('data/processed/clean_transactions.parquet')
WHERE customer_id IS NOT NULL;

-- 2. Account Dimension
CREATE OR REPLACE TABLE dim_account AS
SELECT DISTINCT
    account_id
FROM read_parquet('data/processed/clean_transactions.parquet')
WHERE account_id IS NOT NULL;

-- 3. Date Dimension
CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT
    CAST(transaction_timestamp AS DATE) AS transaction_date,
    EXTRACT(YEAR FROM transaction_timestamp) AS year,
    EXTRACT(MONTH FROM transaction_timestamp) AS month,
    EXTRACT(QUARTER FROM transaction_timestamp) AS quarter,
    EXTRACT(DAY FROM transaction_timestamp) AS day
FROM read_parquet('data/processed/clean_transactions.parquet')
WHERE transaction_timestamp IS NOT NULL;

-- 4. Merchant Dimension
CREATE OR REPLACE TABLE dim_merchant AS
SELECT DISTINCT
    merchant_name,
    merchant_category,
    city,
    country
FROM read_parquet('data/processed/clean_transactions.parquet')
WHERE merchant_name IS NOT NULL;

-- 5. Fact Transactions
CREATE OR REPLACE TABLE fact_transactions AS
SELECT
    transaction_id,
    customer_id,
    account_id,
    CAST(transaction_timestamp AS DATE) AS transaction_date,
    merchant_name,
    amount,
    currency,
    transaction_type,
    payment_method,
    status,
    fraud_flag
FROM read_parquet('data/processed/clean_transactions.parquet');