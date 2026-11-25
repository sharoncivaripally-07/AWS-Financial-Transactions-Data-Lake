from pathlib import Path
import duckdb

# Locate the project folder
project_folder = Path(__file__).resolve().parent

# Locate the Star Schema SQL file
sql_file = project_folder / "sql" / "star_schema.sql"

# Create a DuckDB database
database_file = project_folder / "financial_warehouse.duckdb"
connection = duckdb.connect(str(database_file))

# Read and execute the SQL
sql_text = sql_file.read_text()
connection.execute(sql_text)

print("Star Schema created successfully!")

# Display the created tables
tables = connection.execute("SHOW TABLES").fetchdf()
print("\nTables created:")
print(tables.to_string(index=False))

connection.close()