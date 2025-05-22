import duckdb
import pandas as pd

# Connexion à la base DuckDB
con = duckdb.connect("data/processed/yellow_taxi.duckdb")

# Lister toutes les tables
print("📋 Tables disponibles :")
print(con.execute("SHOW TABLES").df())

# Vérifier et afficher les contenus
def preview_table(table_name):
    try:
        count = con.execute(f"SELECT COUNT(*) AS n FROM {table_name}").df().iloc[0]["n"]
        print(f"\n✅ {table_name} : {int(count)} lignes")
        print(con.execute(f"SELECT * FROM {table_name} LIMIT 5").df())
    except Exception as e:
        print(f"⚠️ {table_name} : erreur de lecture → {e}")

# Tables à inspecter
tables_to_check = ["weather_hourly", "yellow_tripdata_2024_01"]

for t in tables_to_check:
    preview_table(t)
