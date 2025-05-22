# scripts/check_weather_dates.py
import duckdb

con = duckdb.connect("data/processed/yellow_taxi.duckdb")

min_max = con.execute("""
    SELECT MIN(timestamp), MAX(timestamp)
    FROM weather_hourly
""").fetchall()

print("🕒 Plage temporelle des données météo :", min_max)
