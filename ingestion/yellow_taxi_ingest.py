import os
import requests

def download_yellow_taxi_data(output_path):
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"

    # S'assurer que le dossier existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"📥 Téléchargement depuis : {url}")
    response = requests.get(url)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Fichier sauvegardé : {output_path}")
    else:
        raise Exception(f"❌ Échec du téléchargement : {response.status_code}")
