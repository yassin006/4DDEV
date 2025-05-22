import os
import json
import duckdb
import pandas as pd
from datetime import datetime

# 📁 Dossier contenant les fichiers JSON météo
weather_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "weather"))

# 📋 Liste des lignes de données
rows = []

# 🔁 Parcours des fichiers JSON météo
for filename in sorted(os.listdir(weather_folder)):
    if filename.endswith(".json"):
        path = os.path.join(weather_folder, filename)
        with open(path, "r") as f:
            try:
                data = json.load(f)

                # Extraire la date depuis le nom de fichier
                timestamp = filename.replace("weather_", "").replace(".json", "")
                timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H-%M-%S")

                # Extraire les données météo
                temp = data.get("main", {}).get("temp")
                weather = data.get("weather", [{}])[0].get("main")

                # Extraire les coordonnées géographiques (si présentes)
                lat = data.get("coord", {}).get("lat")
                lon = data.get("coord", {}).get("lon")

                rows.append({
                    "timestamp": timestamp,
                    "temp": temp,
                    "weather": weather,
                    "lat": lat,
                    "lon": lon
                })
            except Exception as e:
                print(f"⚠️ Erreur dans {filename}: {e}")

# ✅ Convertir en DataFrame
df = pd.DataFrame(rows)

# 💾 Connexion à DuckDB
duckdb_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "processed", "yellow_taxi.duckdb"))
con = duckdb.connect(duckdb_file)

# 🔄 Écrire dans une table weather_hourly
con.execute("DROP TABLE IF EXISTS weather_hourly")
con.execute("CREATE TABLE weather_hourly AS SELECT * FROM df")

print("✅ Données météo chargées dans DuckDB (weather_hourly)")
