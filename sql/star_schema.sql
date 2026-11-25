-- AWS Financial Transactions Data Lake
-- Star Schema Data Warehouse
-- Version 2: Surrogate Keys and Relationships

-- 1. Customer Dimension
CREATE OR REPLACE TABLE dim_customer AS
SELECT
    ROW_NUMBER() OVER (ORDER BY customer_id) AS customer_key,
    customer_id
FROM (
    SELECT DISTINCT customer_id
    FROM read_parquet('data/processed/clean_transactions.parquet')
    WHERE customer_id IS NOT NULL
);

-- 2. Account Dimension
CREATE OR REPLACE TABLE dim_account AS
SELECT
    ROW_NUMBER() OVER (ORDER BY account_id) AS account_key,
    account_id
FROM (
    SELECT DISTINCT account_id
    FROM read_parquet('data/processed/clean_transactions.parquet')
    WHERE account_id IS NOT NULL
);

-- 3. Date Dimension
CREATE OR REPLACE TABLE dim_date AS
SELECT
    ROW_NUMBER() OVER (ORDER BY transaction_date) AS date_key,
    transaction_date,
    EXTRACT(YEAR FROM transaction_date) AS year,
    EXTRACT(MONTH FROM transaction_date) AS month,
    EXTRACT(QUARTER FROM transaction_date) AS quarter,
    EXTRACT(DAY FROM transaction_date) AS day
FROM (
    SELECT DISTINCT
        CAST(transaction_timestamp AS DATE) AS transaction_date
    FROM read_parquet('data/processed/clean_transactions.parquet')
    WHERE transaction_timestamp IS NOT NULL
);

-- 4. Merchant Dimension
CREATE OR REPLACE TABLE dim_merchant AS
SELECT
    ROW_NUMBER() OVER (
        ORDER BY merchant_name, merchant_category, city, country
    ) AS merchant_key,
    merchant_name,
    merchant_category,
    city,
    country
FROM (
    SELECT DISTINCT
        merchant_name,
        merchant_category,
        city,
        country
    FROM read_parquet('data/processed/clean_transactions.parquet')
);

-- 5. Fact Transactions
CREATE OR REPLACE TABLE fact_transactions AS
SELECT
    t.transaction_id,
    c.customer_key,
    a.account_key,
    d.date_key,
    m.merchant_key,
    t.amount,
    t.currency,
    t.transaction_type,
    t.payment_method,
    t.status,
    t.fraud_flag
FROM read_parquet('data/processed/clean_transactions.parquet') t

LEFT JOIN dim_customer c
    ON t.customer_id = c.customer_id

LEFT JOIN dim_account a
    ON t.account_id = a.account_id

LEFT JOIN dim_date d
    ON CAST(t.transaction_timestamp AS DATE) = d.transaction_date

LEFT JOIN dim_merchant m
    ON t.merchant_name IS NOT DISTINCT FROM m.merchant_name
    AND t.merchant_category IS NOT DISTINCT FROM m.merchant_category
    AND t.city IS NOT DISTINCT FROM m.city
    AND t.country IS NOT DISTINCT FROM m.country;