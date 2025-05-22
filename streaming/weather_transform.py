from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, when, hour, dayofweek

# Créer la session Spark
spark = SparkSession.builder \
    .appName("Taxi Trip Data Transformation") \
    .getOrCreate()

# Chemin vers les données brutes
INPUT_PATH = "data/raw/yellow_taxi/"
JDBC_URL = "jdbc:postgresql://postgres:5432/airflow"
JDBC_USER = "airflow"
JDBC_PASSWORD = "airflow"
TABLE_NAME = "fact_taxi_trips"

# Lire les données parquet
df = spark.read.parquet(INPUT_PATH)

# Transformation des données
df_cleaned = df \
    .withColumn("pickup_datetime", to_timestamp(col("tpep_pickup_datetime"))) \
    .withColumn("dropoff_datetime", to_timestamp(col("tpep_dropoff_datetime"))) \
    .withColumn("trip_duration", (col("dropoff_datetime").cast("long") - col("pickup_datetime").cast("long")) / 60) \
    .withColumn("distance_range", when(col("trip_distance") <= 2, "0-2 km")
                .when((col("trip_distance") > 2) & (col("trip_distance") <= 5), "2-5 km")
                .otherwise(">5 km")) \
    .withColumn("tip_pct", when(col("fare_amount") > 0, (col("tip_amount") / col("fare_amount")) * 100).otherwise(0)) \
    .withColumn("pickup_hour", hour(col("pickup_datetime"))) \
    .withColumn("pickup_day", dayofweek(col("pickup_datetime")))

# Sauvegarde dans PostgreSQL
df_cleaned.write \
    .format("jdbc") \
    .option("url", JDBC_URL) \
    .option("dbtable", TABLE_NAME) \
    .option("user", JDBC_USER) \
    .option("password", JDBC_PASSWORD) \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()

print("✅ Données de taxi transformées et stockées dans PostgreSQL.")
