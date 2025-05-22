import duckdb
import os
from pyspark.sql import SparkSession

# Chemin vers le fichier parquet
PARQUET_PATH = "data/raw/yellow_taxi/yellow_tripdata_2024-01.parquet"
DUCKDB_PATH = "data/processed/yellow_taxi.duckdb"
TABLE_NAME = "yellow_tripdata_2024_01"

# Vérification d'existence du fichier
if not os.path.exists(PARQUET_PATH):
    raise FileNotFoundError(f"❌ Fichier introuvable : {PARQUET_PATH}")

# Créer une session Spark pour lire le fichier parquet
spark = SparkSession.builder.appName("Load Taxi to DuckDB").getOrCreate()
df = spark.read.parquet(PARQUET_PATH)

# Nettoyage minimum (suppression des lignes sans date de pickup)
df_clean = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])

# Convertir en DataFrame pandas
df_pd = df_clean.toPandas()

# Connexion à DuckDB et insertion
with duckdb.connect(DUCKDB_PATH) as con:
    con.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
    con.execute(f"CREATE TABLE {TABLE_NAME} AS SELECT * FROM df_pd")

print("✅ Données taxi chargées dans DuckDB :", TABLE_NAME)
