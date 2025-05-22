import requests
import json
import os
from datetime import datetime

API_KEY = "9c736282847e56ed70d2a43c3ddfac99" 
CITY = "New York"
FOLDER_PATH = "data/raw/weather/"
os.makedirs(FOLDER_PATH, exist_ok=True)

def fetch_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        filename = os.path.join(FOLDER_PATH, f"weather_{timestamp}.json")
        with open(filename, "w") as f:
            json.dump(data, f)
        print(f"[✓] Données météo sauvegardées : {filename}")
    else:
        print(f"[✗] Erreur API météo : {response.status_code}")
