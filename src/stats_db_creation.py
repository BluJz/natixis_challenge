import pandas as pd
import sqlite3

# Step 1: Read CSV file into DataFrame
csv_file_path = "RFQ_Data_Challenge_HEC.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path, dtype={7: "str", 9: "str"})

# Renommer les duplicates
df.rename(columns={"Cusip": "cusip2", "Maturity": "maturity2"}, inplace=True)

# Step 2: Create SQLite database
db_file_path = "src/pages/natixis.db"  # Replace with your desired .db file path
conn = sqlite3.connect(db_file_path)

# Step 3: Write DataFrame to SQLite database
df.to_sql(
    "ma_table", conn, if_exists="replace", index=False
)  # Replace 'table_name' with your desired table name

# Close the connection
conn.close()
