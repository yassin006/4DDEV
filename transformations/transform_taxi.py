def transform_yellow_taxi_data():
    from pyspark.sql import SparkSession
    import duckdb
    import os

    spark = SparkSession.builder \
        .appName("Yellow Taxi Parquet to DuckDB") \
        .getOrCreate()

    parquet_file = "data/raw/yellow_taxi/yellow_tripdata_2024-01.parquet"
    if not os.path.exists(parquet_file):
        print(f"❌ Le fichier {parquet_file} n'existe pas.")
        return

    df = spark.read.parquet(parquet_file)
    df_clean = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
    df_pd = df_clean.toPandas()

    duckdb_file = "data/processed/yellow_taxi.duckdb"
    with duckdb.connect(duckdb_file) as con:
        con.execute("DROP TABLE IF EXISTS yellow_tripdata_2024_01")
        con.execute("CREATE TABLE yellow_tripdata_2024_01 AS SELECT * FROM df_pd")

    print("✅ Données transformées et stockées dans DuckDB")
