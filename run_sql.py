from pathlib import Path
import duckdb

# Find the SQL file
project_folder = Path(__file__).resolve().parent
sql_file = project_folder / "sql" / "financial_analysis.sql"

# Connect to DuckDB
connection = duckdb.connect()

# Read the SQL file
sql_text = sql_file.read_text()

# Execute each SQL query
for number, query in enumerate(sql_text.split(";"), start=1):
    if query.strip():
        print(f"\n--- SQL Query {number} ---")
        result = connection.execute(query).fetchdf()
        print(result.to_string(index=False))

# Close the connection
connection.close()

print("\nAll SQL queries executed successfully!")