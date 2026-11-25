
-- AWS Financial Transactions Data Lake
-- Financial Transaction Analytics
-- Data source: clean_transactions.parquet

-- 1. Total transaction amount and transaction count
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_transaction_amount,
    AVG(amount) AS average_transaction_amount
FROM read_parquet('data/processed/clean_transactions.parquet');


-- 2. Monthly transaction volume and amount
SELECT
    DATE_TRUNC('month', transaction_timestamp) AS transaction_month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS monthly_transaction_amount
FROM read_parquet('data/processed/clean_transactions.parquet')
GROUP BY transaction_month
ORDER BY transaction_month;


-- 3. Top 10 customers by total transaction amount
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spending
FROM read_parquet('data/processed/clean_transactions.parquet')
GROUP BY customer_id
ORDER BY total_spending DESC
LIMIT 10;


-- 4. Transaction volume by account
SELECT
    account_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_transaction_amount
FROM read_parquet('data/processed/clean_transactions.parquet')
GROUP BY account_id
ORDER BY transaction_count DESC;


-- 5. Transaction analysis by merchant category
SELECT
    merchant_category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_transaction_amount,
    AVG(amount) AS average_transaction_amount
FROM read_parquet('data/processed/clean_transactions.parquet')
GROUP BY merchant_category
ORDER BY total_transaction_amount DESC;
