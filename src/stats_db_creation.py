import pandas as pd
import sqlite3
import os

# Step 1: Read CSV file into DataFrame
csv_file_path = "RFQ_Data_Challenge_HEC.csv"  # Replace with your CSV file path
df = pd.read_csv(csv_file_path, dtype={7: "str", 9: "str"})

# Renommer les duplicates
df.rename(columns={"Cusip": "cusip2", "Maturity": "maturity2"}, inplace=True)

folder_path = 'src/stats'

# Vérifier si le dossier existe déjà
if not os.path.exists(folder_path):
    # Créer le dossier
    os.makedirs(folder_path)
    
    # Créer un fichier .gitkeep dans le dossier
    open(os.path.join(folder_path, '.gitkeep'), 'a').close()

    # Utiliser Git pour ajouter et commiter le dossier
    os.system(f'git add {folder_path}/.gitkeep')
    os.system('git commit -m "Ajout du nouveau dossier"')
    os.system('git push')
else:
    print("Le dossier existe déjà.")

# Step 2: Create SQLite database
db_file_path = "src/stats/stats.db"  # Replace with your desired .db file path
conn = sqlite3.connect(db_file_path)

# Step 3: Write DataFrame to SQLite database
df.to_sql(
    "ma_table", conn, if_exists="replace", index=False
)  # Replace 'table_name' with your desired table name

# Close the connection
conn.close()
