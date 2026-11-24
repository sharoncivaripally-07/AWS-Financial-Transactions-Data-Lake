# AWS Financial Transactions Data Lake

## Project Overview

This project demonstrates an end-to-end financial transaction data processing pipeline using Python, Pandas, and Parquet.

The pipeline processes raw financial transaction data, performs data cleaning and validation, separates valid and rejected records, and stores the processed data in structured formats for analytics.

## Project Objectives

- Build a Python-based ETL pipeline.
- Process raw financial transaction data.
- Perform data quality checks.
- Identify and remove duplicate records.
- Separate valid and rejected transactions.
- Store clean data in Parquet format.

## Technologies Used

- Python 3
- Pandas
- PyArrow
- CSV
- Apache Parquet
- Git and GitHub

## Project Architecture

```text
Raw Financial Data (CSV)
          |
          v
    Python ETL Pipeline
          |
          v
   Data Cleaning & Validation
          |
          v
     Data Quality Checks
          |
       /     \
      v       v
 Valid Data  Rejected Data
      |       |
      v       v
  Parquet     CSV
```

## Data Processing Results

The pipeline processed 1,000 financial transaction records.

| Metric | Result |
|---|---:|
| Total records received | 1,000 |
| Valid records | 942 |
| Rejected records | 58 |

## Data Quality Checks

The pipeline performs the following checks:

- Validates missing values.
- Checks transaction amount values.
- Validates timestamp formats.
- Identifies duplicate records.
- Separates invalid records for review.

## Project Structure

```text
AWS-Financial-Transactions-Data-Lake/
│
├── data/
│   ├── raw/
│   │   └── financial_transactions.csv
│   │
│   └── processed/
│       ├── clean_transactions.parquet
│       └── rejected_transactions.csv
│
├── src/
│   └── transformation/
│       └── clean_transactions.py
│
├── generate_data.py
├── data-quality-rules.md
├── README.md
└── .gitignore
```

## How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/sharoncivaripally-07/AWS-Financial-Transactions-Data-Lake.git
```

2. Navigate to the project folder:

```bash
cd AWS-Financial-Transactions-Data-Lake
```

3. Install dependencies:

```bash
pip install pandas pyarrow
```

4. Run the ETL pipeline:

```bash
python3 src/transformation/clean_transactions.py
```

## Future Enhancements

- Integrate AWS S3 for cloud storage.
- Use AWS Glue for scalable ETL processing.
- Query processed data using Amazon Athena.
- Add automated data quality testing.
- Implement workflow orchestration using AWS Step Functions.

## Author

**Sharon Civaripally**

Data Engineer | Python | SQL | AWS | ETL | Data Pipelines
